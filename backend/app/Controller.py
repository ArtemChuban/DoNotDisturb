import ydb  # type: ignore
import uuid
from fastapi import HTTPException, status
from models import User
from utils import hash_password, verify_password
import os


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

    @staticmethod
    def callee(session: ydb.Session, query: str):
        return session.transaction().execute(
            query,
            commit_tx=True,
            settings=ydb.BaseRequestSettings()
            .with_timeout(3)
            .with_operation_timeout(2),
        )

    def username_exist(self, username: str) -> bool:
        query = (
            f"select count(*) as `count` from Users where `username` = '{username}';"
        )
        count = (
            self.__session_pool.retry_operation_sync(self.callee, query=query)[0]
            .rows[0]
            .count
        )
        return count > 0

    def try_register(self, username: str, password: str) -> str:
        if self.username_exist(username):
            raise HTTPException(status.HTTP_409_CONFLICT)
        user = User(username=username, password=hash_password(password))
        query = f"insert into Users (id, username, password) \
            values ('{user.id}', '{user.username}', '{user.password}');"
        self.__session_pool.retry_operation_sync(self.callee, query=query)
        return self.create_session(user.id)

    def create_session(self, user_id: str) -> str:
        user_session = str(uuid.uuid4())
        query = f"insert into Sessions (user_id, session) \
                  values ('{user_id}', '{user_session}');"
        self.__session_pool.retry_operation_sync(self.callee, query=query)
        return user_session

    def try_login(self, username: str, password: str) -> str:
        query = f"select id, password from Users where `username` = '{username}';"
        users = self.__session_pool.retry_operation_sync(self.callee, query=query)[
            0
        ].rows
        if len(users) == 0:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        user = users[0]
        hashed_password = user.password
        if not verify_password(password, hashed_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return self.create_session(user.id)
