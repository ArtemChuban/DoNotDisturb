import os
import uuid

import jwt
import ydb  # type: ignore
from fastapi import HTTPException, status
from schemas import MemberInfo, TeamInfo, UserInfo
from utils import hash_password, verify_password


class Controller:
    __driver: ydb.Driver
    __session_pool: ydb.SessionPool
    __jwt_key: str

    def start(self) -> None:
        endpoint = os.getenv("ENDPOINT")
        database = os.getenv("DATABASE")
        jwt_key = os.getenv("SECRET_KEY")
        if jwt_key is None:
            raise ValueError("SECRET_KEY environment variable not set")
        self.__jwt_key = jwt_key
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

    def get_user(self, jwtoken: str) -> UserInfo:
        user_id = self.__get_user_id_by_jwt(jwtoken)
        username = self.__get_username_by_id(user_id)
        teams = self.__get_teams_info_by_user_id(user_id)
        invites = self.__get_invites_info_by_user_id(user_id)
        balance = self.__get__balance(user_id)
        return UserInfo(
            username=username,
            teams=teams,
            invites=invites,
            balance=balance,
        )

    def get_members(self, jwtoken: str, team_id: str) -> list[MemberInfo]:
        user_id = self.__get_user_id_by_jwt(jwtoken)
        if not self.__is_user_in_team(user_id, team_id):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        return self.__get_members(team_id)

    def register(self, username: str, password: str) -> str:
        if self.__username_exist(username):
            raise HTTPException(status.HTTP_409_CONFLICT)
        user_id = self.__create_user(username, password)
        jwtoken = self.__create_jwt(user_id)
        return jwtoken

    def login(self, username: str, password: str) -> str:
        user_id = self.__get_user_id_by_username_and_password(username, password)
        jwtoken = self.__create_jwt(user_id)
        return jwtoken

    def create_team(self, jwtoken: str, name: str) -> str:
        user_id = self.__get_user_id_by_jwt(jwtoken)
        team_creation_price = 1  # TODO: env var
        self.__change_balance(user_id, -team_creation_price)
        team_id = self.__create_team(user_id, name)
        self.__add_member(user_id, team_id, is_admin=True)
        return team_id

    def invite(self, jwtoken: str, team_id: str, username: str) -> None:
        initiator_id = self.__get_user_id_by_jwt(jwtoken)
        if not self.__user_is_admin(initiator_id, team_id):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        user_id = self.__get_user_id_by_username(username)
        if self.__member_exist(user_id, team_id):
            raise HTTPException(status.HTTP_409_CONFLICT)
        self.__invite(user_id, team_id)

    def invite_reply(self, jwtoken: str, team_id: str, accepted: bool) -> None:
        user_id = self.__get_user_id_by_jwt(jwtoken)
        if not self.__invite_exist(user_id, team_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        self.__remove_invite(user_id, team_id)
        if accepted:
            self.__add_member(user_id, team_id)

    def reward(self, jwtoken: str, team_id: str, user_id: str, value: int) -> None:
        initiator_id = self.__get_user_id_by_jwt(jwtoken)
        if not self.__user_is_admin(initiator_id, team_id):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        self.__change_tokens(user_id, team_id, value)

    def transfer(self, jwtoken: str, team_id: str, user_id: str, value: int) -> None:
        initiator_id = self.__get_user_id_by_jwt(jwtoken)
        self.__change_tokens(initiator_id, team_id, -value)
        self.__change_tokens(user_id, team_id, value)

    def update_user(self, jwtoken: str, new_password: str) -> None:
        user_id = self.__get_user_id_by_jwt(jwtoken)
        self.__change_password(user_id, new_password)

    @staticmethod
    def __callee(
        session: ydb.Session, query: str, parameters: dict[str, str] | None = None
    ):
        return session.transaction().execute(
            session.prepare(query),
            parameters=parameters,
            commit_tx=True,
            settings=ydb.BaseRequestSettings()
            .with_timeout(3)
            .with_operation_timeout(2),
        )

    def __change_tokens(self, user_id: str, team_id: str, value: int) -> None:
        if value < 0:
            old_tokens = self.__get__tokens(user_id, team_id)
            new_tokens = old_tokens + value
            if new_tokens < 0:
                raise HTTPException(status.HTTP_400_BAD_REQUEST)
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                declare $value as Int64;
                update Membership
                set `tokens` = cast(cast(`tokens` as Int64) + $value as Uint64)
                where `user_id` = $userId and `team_id` = $teamId;
                """
        self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$teamId": team_id, "$value": value},
        )

    def __change_balance(self, user_id: str, value: int) -> None:
        if value >= 0:
            raise NotImplementedError
        old_balance = self.__get__balance(user_id)
        new_balance = old_balance + value
        if new_balance < 0:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        query = """
                declare $userId as utf8;
                declare $value as Int64;
                update Users
                set `balance` = cast(cast(`balance` as Int64) + $value as Uint64)
                where `id` = $userId;
                """
        self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$value": value},
        )

    def __change_password(self, user_id: str, new_password: str) -> None:
        hashed_password = hash_password(new_password)
        query = """
                declare $userId as utf8;
                declare $password as utf8;
                update Users
                set `password` = $password
                where `id` = $userId;
                """
        self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$password": hashed_password},
        )

    def __get__tokens(self, user_id: str, team_id: str) -> int:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                select tokens from Membership
                where `user_id` = $userId and `team_id` = $teamId;
                """
        rows = self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$teamId": team_id},
        )[0].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return rows[0].tokens

    def __get__balance(self, user_id: str) -> int:
        query = """
                declare $userId as utf8;
                select balance from Users
                where `id` = $userId;
                """
        rows = self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id},
        )[0].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return rows[0].balance

    def __create_user(self, username: str, password: str) -> str:
        hashed_password = hash_password(password)
        user_id = str(uuid.uuid4())
        query = """
                declare $userId as utf8;
                declare $username as utf8;
                declare $password as utf8;
                insert into Users (id, username, password, balance)
                values ($userId, $username, $password, 0);
                """
        self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={
                "$userId": user_id,
                "$username": username,
                "$password": hashed_password,
            },
        )
        return user_id

    def __invite_exist(self, user_id: str, team_id: str) -> bool:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                select count(*) as `count` from Invites
                where `user_id` = $userId and `team_id` = $teamId;
                """
        count = (
            self.__session_pool.retry_operation_sync(
                self.__callee,
                query=query,
                parameters={"$userId": user_id, "$teamId": team_id},
            )[0]
            .rows[0]
            .count
        )
        return count > 0

    def __remove_invite(self, user_id: str, team_id: str) -> None:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                delete from Invites
                where `user_id` = $userId and `team_id` = $teamId;
                """
        self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$teamId": team_id},
        )

    def __get_teams_info_by_user_id(self, user_id: str) -> list[TeamInfo]:
        query = """
                declare $userId as utf8;
                select Teams.name as name, Membership.team_id as id
                from Membership inner join Teams on Membership.team_id = Teams.id
                where `user_id` = $userId;
                """
        teams = self.__session_pool.retry_operation_sync(
            self.__callee, query=query, parameters={"$userId": user_id}
        )[0].rows
        return [TeamInfo(name=team.name, id=team.id) for team in teams]

    def __get_invites_info_by_user_id(self, user_id: str) -> list[TeamInfo]:
        query = """
                declare $userId as utf8;
                select Teams.name as name, Invites.team_id as id
                from Invites inner join Teams on Invites.team_id = Teams.id
                where `user_id` = $userId;
                """
        teams = self.__session_pool.retry_operation_sync(
            self.__callee, query=query, parameters={"$userId": user_id}
        )[0].rows
        return [TeamInfo(name=team.name, id=team.id) for team in teams]

    def __get_username_by_id(self, user_id: str) -> str:
        query = """
                declare $userId as utf8;
                select username from Users where `id` = $userId;
                """
        users = self.__session_pool.retry_operation_sync(
            self.__callee, query=query, parameters={"$userId": user_id}
        )[0].rows
        if len(users) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return users[0].username

    def __get_user_id_by_username_and_password(
        self, username: str, password: str
    ) -> str:
        query = """
                declare $username as utf8;
                select id, password from Users where `username` = $username;
                """
        users = self.__session_pool.retry_operation_sync(
            self.__callee, query=query, parameters={"$username": username}
        )[0].rows
        if len(users) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        user = users[0]
        hashed_password = user.password
        if not verify_password(password, hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return user.id

    def __username_exist(self, username: str) -> bool:
        query = """
                declare $username as utf8;
                select count(*) as `count` from Users where `username` = $username;
                """
        count = (
            self.__session_pool.retry_operation_sync(
                self.__callee, query=query, parameters={"$username": username}
            )[0]
            .rows[0]
            .count
        )
        return count > 0

    def __get_user_id_by_username(self, username: str) -> str:
        query = """
                declare $username as utf8;
                select `id` from Users where `username` = $username;
                """
        rows = self.__session_pool.retry_operation_sync(
            self.__callee, query=query, parameters={"$username": username}
        )[0].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return rows[0].id

    def __team_name_exist(self, name: str) -> bool:
        query = """
                declare $name as utf8;
                select count(*) as `count` from Teams where `name` = $name;
                """
        count = (
            self.__session_pool.retry_operation_sync(
                self.__callee, query=query, parameters={"$name": name}
            )[0]
            .rows[0]
            .count
        )
        return count > 0

    def __get_user_id_by_jwt(self, session: str) -> str:
        try:
            return jwt.decode(session, self.__jwt_key, algorithms=["HS256"])["id"]
        except jwt.PyJWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    def __create_jwt(self, user_id: str) -> str:
        return jwt.encode({"id": user_id}, self.__jwt_key, algorithm="HS256")

    def __create_team(self, user_id: str, name: str) -> str:
        if self.__team_name_exist(name):
            raise HTTPException(status.HTTP_409_CONFLICT)
        team_id = str(uuid.uuid4())
        query = """
                declare $teamId as utf8;
                declare $name as utf8;
                insert into Teams (id, name) values ($teamId, $name);
                """
        self.__session_pool.retry_operation_sync(
            self.__callee, query=query, parameters={"$teamId": team_id, "$name": name}
        )
        return team_id

    def __member_exist(self, user_id: str, team_id: str) -> bool:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                select count(*) as `count` from Membership
                where `user_id` = $userId and `team_id` = $teamId;
                """
        count = (
            self.__session_pool.retry_operation_sync(
                self.__callee,
                query=query,
                parameters={"$userId": user_id, "$teamId": team_id},
            )[0]
            .rows[0]
            .count
        )
        return count > 0

    def __add_member(self, user_id: str, team_id: str, is_admin: bool = False) -> None:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                declare $isAdmin as bool;
                insert into Membership (user_id, team_id, is_admin, tokens)
                values ($userId, $teamId, $isAdmin, 0);
                """
        self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$teamId": team_id, "$isAdmin": is_admin},
        )

    def __user_is_admin(self, user_id: str, team_id: str) -> bool:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                select `is_admin` from Membership
                where `user_id` = $userId and `team_id` = $teamId;
                """
        rows = self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$teamId": team_id},
        )[0].rows
        if len(rows) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return rows[0].is_admin

    def __invite(self, user_id: str, team_id: str) -> None:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                insert into Invites (user_id, team_id) values ($userId, $teamId);
                """

        self.__session_pool.retry_operation_sync(
            self.__callee,
            query=query,
            parameters={"$userId": user_id, "$teamId": team_id},
        )

    def __get_members(self, team_id: str) -> list[MemberInfo]:
        query = """
                declare $teamId as utf8;
                select
                Users.id as id,
                Users.username as username,
                Membership.is_admin as is_admin,
                Membership.tokens as tokens
                from Membership inner join Users on Membership.user_id = Users.id
                where `team_id` = $teamId;
                """
        users = self.__session_pool.retry_operation_sync(
            self.__callee, query=query, parameters={"$teamId": team_id}
        )[0].rows
        return [
            MemberInfo(
                id=user.id,
                username=user.username,
                is_admin=user.is_admin,
                tokens=user.tokens,
            )
            for user in users
        ]

    def __is_user_in_team(self, user_id: str, team_id: str) -> bool:
        query = """
                declare $userId as utf8;
                declare $teamId as utf8;
                select count(*) as count from Membership
                where `user_id` = $userId and `team_id` = $teamId;
                """
        count = (
            self.__session_pool.retry_operation_sync(
                self.__callee,
                query=query,
                parameters={"$userId": user_id, "$teamId": team_id},
            )[0]
            .rows[0]
            .count
        )
        return count > 0
