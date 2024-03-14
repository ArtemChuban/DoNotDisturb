import ydb  # type: ignore
import uuid
from fastapi import HTTPException, status
from utils import hash_password, verify_password
import os
from schemas import UserInfo, TeamInfo


class Controller:
    __driver: ydb.Driver
    __session_pool: ydb.SessionPool

    def start(self) -> None:
        endpoint = os.getenv("ENDPOINT")
        database = os.getenv("DATABASE")
        if endpoint is None:
            raise ValueError("ENDPOINT environment variable not set")
        if database is None:
            raise ValueError("DATABASE environment variable not set")
        self.__driver = ydb.Driver(
            endpoint=endpoint,
            database=database,
            credentials=ydb.credentials_from_env_variables(),
        )
        self.__driver.wait(timeout=10, fail_fast=True)
        self.__session_pool = ydb.SessionPool(self.__driver)

    def stop(self) -> None:
        self.__session_pool.stop()
        self.__driver.stop()

    def get_user(self, session: str) -> UserInfo:
        user_id = self.__get_user_id_by_session(session)
        username = self.__get_username_by_id(user_id)
        teams = self.__get_teams_info_by_user_id(user_id)
        invites = self.__get_invites_info_by_user_id(user_id)
        return UserInfo(username=username, teams=teams, invites=invites)

    def register(self, username: str, password: str) -> str:
        if self.__username_exist(username):
            raise HTTPException(status.HTTP_409_CONFLICT)
        user_id = self.__create_user(username, password)
        session = self.__create_session(user_id)
        return session

    def login(self, username: str, password: str) -> str:
        user_id = self.__get_user_id_by_username_and_password(username, password)
        session = self.__create_session(user_id)
        return session

    def create_team(self, session: str, name: str) -> str:
        user_id = self.__get_user_id_by_session(session)
        team_id = self.__create_team(user_id, name)
        self.__add_member(user_id, team_id, is_admin=True)
        return team_id

    def invite(self, session: str, team_id: str, username: str) -> None:
        initiator_id = self.__get_user_id_by_session(session)
        if not self.__user_is_admin(initiator_id, team_id):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        user_id = self.__get_user_id_by_username(username)
        if self.__member_exist(user_id, team_id):
            raise HTTPException(status.HTTP_409_CONFLICT)
        self.__invite(user_id, team_id)

    def invite_reply(self, session: str, team_id: str, accepted: bool) -> None:
        user_id = self.__get_user_id_by_session(session)
        if not self.__invite_exist(user_id, team_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        self.__remove_invite(user_id, team_id)
        if accepted:
            self.__add_member(user_id, team_id)

    def reward(self, session: str, team_id: str, user_id: str, value: int) -> None:
        if value <= 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        initiator_id = self.__get_user_id_by_session(session)
        if not self.__user_is_admin(initiator_id, team_id):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        self.__change_tokens(user_id, team_id, value)

    def transfer(self, session: str, team_id: str, user_id: str, value: int) -> None:
        if value <= 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        initiator_id = self.__get_user_id_by_session(session)
        self.__change_tokens(initiator_id, team_id, -value)
        self.__change_tokens(user_id, team_id, value)

    @staticmethod
    def __callee(session: ydb.Session, query: str):
        return session.transaction().execute(
            query,
            commit_tx=True,
            settings=ydb.BaseRequestSettings()
            .with_timeout(3)
            .with_operation_timeout(2),
        )

    def __change_tokens(self, user_id: str, team_id: str, value: int) -> None:
        old_tokens = self.__get__tokens(user_id, team_id)
        new_tokens = old_tokens + value
        if new_tokens < 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        query = f"update Membership \
                set `tokens` = `tokens` + {value} \
                where `user_id` = '{user_id}' and `team_id` = '{team_id}';"
        self.__session_pool.retry_operation_sync(self.__callee, query=query)

    def __get__tokens(self, user_id: str, team_id: str) -> int:
        query = f"select tokens from Membership \
                where `user_id` = '{user_id}' and `team_id` = '{team_id}';"
        rows = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return rows[0].tokens

    def __create_user(self, username: str, password: str) -> str:
        hashed_password = hash_password(password)
        user_id = str(uuid.uuid4())
        query = f"insert into Users (id, username, password) \
            values ('{user_id}', '{username}', '{hashed_password}');"
        self.__session_pool.retry_operation_sync(self.__callee, query=query)
        return user_id

    def __invite_exist(self, user_id: str, team_id: str) -> bool:
        query = f"select count(*) as `count` from Invites \
                where `user_id` = '{user_id}' and `team_id` = '{team_id}';"
        count = (
            self.__session_pool.retry_operation_sync(self.__callee, query=query)[0]
            .rows[0]
            .count
        )
        return count > 0

    def __remove_invite(self, user_id: str, team_id: str) -> None:
        query = f"delete from Invites \
                where `user_id` = '{user_id}' and `team_id` = '{team_id}'"
        self.__session_pool.retry_operation_sync(self.__callee, query=query)

    def __get_teams_info_by_user_id(self, user_id: str) -> list[TeamInfo]:
        query = f"select Teams.name as name, Membership.team_id as id \
                from Membership inner join Teams on Membership.team_id = Teams.id \
                where `user_id` = '{user_id}';"
        teams = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        return [TeamInfo(name=team.name, id=team.id) for team in teams]

    def __get_invites_info_by_user_id(self, user_id: str) -> list[TeamInfo]:
        query = f"select Teams.name as name, Invites.team_id as id \
                from Invites inner join Teams on Invites.team_id = Teams.id \
                where `user_id` = '{user_id}';"
        teams = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        return [TeamInfo(name=team.name, id=team.id) for team in teams]

    def __get_username_by_id(self, user_id: str) -> str:
        query = f"select username from Users where `id` = '{user_id}';"
        users = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        if len(users) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return users[0].username

    def __get_user_id_by_username_and_password(
        self, username: str, password: str
    ) -> str:
        query = f"select id, password from Users where `username` = '{username}';"
        users = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        if len(users) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        user = users[0]
        hashed_password = user.password
        if not verify_password(password, hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return user.id

    def __username_exist(self, username: str) -> bool:
        query = (
            f"select count(*) as `count` from Users where `username` = '{username}';"
        )
        count = (
            self.__session_pool.retry_operation_sync(self.__callee, query=query)[0]
            .rows[0]
            .count
        )
        return count > 0

    def __get_user_id_by_username(self, username: str) -> str:
        query = f"select `id` from Users where `username` = '{username}';"
        rows = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return rows[0].id

    def __team_name_exist(self, name: str) -> bool:
        query = f"select count(*) as `count` from Teams where `name` = '{name}';"
        count = (
            self.__session_pool.retry_operation_sync(self.__callee, query=query)[0]
            .rows[0]
            .count
        )
        return count > 0

    def __get_user_id_by_session(self, session: str) -> str:
        query = f"select `user_id` from Sessions where `session` = '{session}';"
        rows = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return rows[0].user_id

    def __create_session(self, user_id: str) -> str:
        user_session = str(uuid.uuid4())
        query = f"insert into Sessions (user_id, session) \
                  values ('{user_id}', '{user_session}');"
        self.__session_pool.retry_operation_sync(self.__callee, query=query)
        return user_session

    def __create_team(self, user_id: str, name: str) -> str:
        if self.__team_name_exist(name):
            raise HTTPException(status.HTTP_409_CONFLICT)
        team_id = str(uuid.uuid4())
        query = f"insert into Teams (id, name) values ('{team_id}', '{name}');"
        self.__session_pool.retry_operation_sync(self.__callee, query=query)
        return team_id

    def __member_exist(self, user_id: str, team_id: str) -> bool:
        query = f"select count(*) as `count` from Membership \
                where `user_id` = '{user_id}' and `team_id` = '{team_id}';"
        count = (
            self.__session_pool.retry_operation_sync(self.__callee, query=query)[0]
            .rows[0]
            .count
        )
        return count > 0

    def __add_member(self, user_id: str, team_id: str, is_admin: bool = False) -> None:
        query = f"insert into Membership (user_id, team_id, is_admin, tokens) \
                values ('{user_id}', '{team_id}', {is_admin}, 0);"
        self.__session_pool.retry_operation_sync(self.__callee, query=query)

    def __user_is_admin(self, user_id: str, team_id: str) -> bool:
        query = f"select `is_admin` from Membership \
                where `user_id` = '{user_id}' and `team_id` = '{team_id}';"
        rows = self.__session_pool.retry_operation_sync(self.__callee, query=query)[
            0
        ].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return rows[0].is_admin

    def __invite(self, user_id: str, team_id: str) -> None:
        query = (
            f"insert into Invites (user_id, team_id) values ('{user_id}', '{team_id}');"
        )
        self.__session_pool.retry_operation_sync(self.__callee, query=query)
