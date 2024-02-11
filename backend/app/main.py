import uuid
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Annotated
from enum import Enum
import time
import re


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if users_collection.find_one({"is_admin": True}) == None:
        admin = User(username="admin", password="admin", is_admin=True)
        users_collection.insert_one(admin.model_dump())
    yield
    # Shutdown
    ...


app = FastAPI(debug=True, lifespan=lifespan, root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongoClient = MongoClient("mongo", 27017)
database = mongoClient["DoNotDisturb"]
users_collection = database["users"]
transactions_collection = database["transactions"]


class UserView(BaseModel):
    username: str
    is_admin: bool = False
    tokens: int = 0


class User(UserView):
    password: str
    sessions: list[str] = []


class TransactionType(str, Enum):
    TRANSFER = "Transfer"
    REWARD = "Reward"


class Transaction(BaseModel):
    timestamp: int
    initiator: str
    reciever: str
    value: int
    type: TransactionType


def get_user_by_session(session: str) -> User:
    result = users_collection.find_one({"sessions": session})
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Wrong session")
    return User(**result)


def get_user_by_username(username: str) -> User:
    result = users_collection.find_one({"username": username})
    if result is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "User with this username not found"
        )
    return User(**result)


def user_exist(username: str) -> bool:
    return users_collection.find_one({"username": username}) is not None


def check_password(password: str) -> None:
    if (
        len(password) < 8
        or re.search(r"\d", password) is None
        or re.search(r"[A-Z]", password) is None
        or re.search(r"[a-z]", password) is None
    ):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too easy password")


@app.post("/users/create")
async def post_users_register(
    session: str, username: Annotated[str, Query(min_length=1)], password: str
) -> None:
    check_password(password)
    user = get_user_by_session(session)
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admin")
    if user_exist(username):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "User with this username not found"
        )

    new_user = User(username=username, password=password)
    users_collection.insert_one(new_user.model_dump())


@app.get("/users")
async def get_users() -> list[UserView]:
    return [UserView(**user) for user in users_collection.find({}).sort("username")]


@app.get("/users/session")
async def get_users_session(username: str, password: str) -> str:
    user = get_user_by_username(username)
    if user.password != password:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Wrong password")

    session = str(uuid.uuid4())
    users_collection.update_one(
        {"username": user.username}, {"$push": {"sessions": session}}
    )
    return session


@app.put("/users/password")
async def put_users_password(session: str, username: str, new_password: str) -> None:
    check_password(new_password)
    current_user = get_user_by_session(session)
    user_to_update = get_user_by_username(username)
    if not current_user.is_admin and current_user.username != user_to_update.username:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Only admin can change password for another user"
        )

    users_collection.update_one(
        {"username": username}, {"$set": {"password": new_password}}
    )


@app.get("/users/by/session")
async def get_users(session: str) -> UserView:
    user = get_user_by_session(session)
    return UserView(**user.model_dump())


@app.get("/users/by/username")
async def get_users(username: str) -> UserView:
    user = get_user_by_username(username)
    return UserView(**user.model_dump())


@app.post("/tokens/reward")
async def post_tokens_reward(
    session: str, username: str, value: Annotated[int, Query(gt=0)]
) -> None:
    current_user = get_user_by_session(session)
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admin can reward")
    if not user_exist(username):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "User with this username not found"
        )

    with mongoClient.start_session() as mongoSession:
        with mongoSession.start_transaction():
            users_collection.update_one(
                {"username": username}, {"$inc": {"tokens": value}}
            )
            transactions_collection.insert_one(
                Transaction(
                    timestamp=int(time.time()),
                    initiator=current_user.username,
                    reciever=username,
                    value=value,
                    type=TransactionType.REWARD,
                ).model_dump()
            )


@app.post("/tokens/transfer")
async def post_tokens_transfer(
    session: str, username: str, value: Annotated[int, Query(gt=0)]
) -> None:
    current_user = get_user_by_session(session)
    if current_user.tokens < value:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "You dont have enough tokens")
    if not user_exist(username):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "User with this username not found"
        )

    with mongoClient.start_session() as mongoSession:
        with mongoSession.start_transaction():
            users_collection.update_one(
                {"username": username}, {"$inc": {"tokens": value}}
            )
            users_collection.update_one(
                {"username": current_user.username}, {"$inc": {"tokens": -value}}
            )
            transactions_collection.insert_one(
                Transaction(
                    timestamp=int(time.time()),
                    initiator=current_user.username,
                    reciever=username,
                    value=value,
                    type=TransactionType.TRANSFER,
                ).model_dump()
            )


@app.get("/transactions")
async def get_transactions(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0)] = 8,
    initiator: str = None,
    reciever: str = None,
) -> list[Transaction]:

    query = {}
    if initiator is not None:
        query["initiator"] = initiator
    if reciever is not None:
        query["reciever"] = reciever
    transactions = (
        transactions_collection.find(query)
        .sort("timestamp", -1)
        .skip(offset)
        .limit(limit)
    )
    return [Transaction(**transaction) for transaction in transactions]
