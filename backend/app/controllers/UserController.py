import re
import uuid

from app.models import User, UserView
from fastapi import HTTPException, status
from pymongo.collection import Collection


class UserController:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def create(self, session: str, username: str, password: str) -> None:
        initiator = self.get_by_session(session)
        if not initiator.is_admin:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admin")
        if self.username_exist(username):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "User with this username already exists"
            )
        new_user = User(username=username, password=password)
        self.collection.insert_one(new_user.model_dump())

    def update_locale(self, session: str, locale: str) -> None:
        user = self.get_by_session(session)
        self.collection.update_one(
            {"username": user.username}, {"$set": {"locale": locale}}
        )

    def update_password(self, session: str, username: str, new_password: str) -> None:
        self.check_password_weakness(new_password)
        initiator = self.get_by_session(session)
        user = self.get_by_username(username)
        if not initiator.is_admin and initiator.username != user.username:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Only admin can change password for another user",
            )
        self.collection.update_one(
            {"username": username}, {"$set": {"password": new_password}}
        )

    def generate_session(self, username: str, password: str) -> str:
        user = self.get_by_username(username)
        if user.password != password:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Wrong password")
        session = str(uuid.uuid4())
        self.collection.update_one(
            {"username": user.username}, {"$push": {"sessions": session}}
        )
        return session

    def get_all(self) -> list[UserView]:
        return [UserView(**user) for user in self.collection.find({}).sort("username")]

    def get_by_session(self, session: str) -> User:
        result = self.collection.find_one({"sessions": session})
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Wrong session")
        return User(**result)

    def get_by_username(self, username: str) -> User:
        result = self.collection.find_one({"username": username})
        if result is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "User with this username not found"
            )
        return User(**result)

    def username_exist(self, username: str) -> bool:
        return self.collection.find_one({"username": username}) is not None

    @staticmethod
    def check_password_weakness(password: str) -> None:
        if (
            len(password) < 8
            or re.search(r"\d", password) is None
            or re.search(r"[A-Z]", password) is None
            or re.search(r"[a-z]", password) is None
        ):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too easy password")

    def check_admin_exist(self) -> None:
        if self.collection.find_one({"is_admin": True}) is not None:
            return
        admin = User(username="admin", password="admin", is_admin=True)
        self.collection.insert_one(admin.model_dump())
