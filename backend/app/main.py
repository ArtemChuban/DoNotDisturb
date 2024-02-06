import uuid
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from contextlib import asynccontextmanager
from enum import Enum
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if users_collection.find_one({"is_admin": True}) == None:
        admin = User(username="admin", password="admin", is_admin=True)
        users_collection.insert_one(admin.model_dump())
    yield
    # Shutdown
    ...


app = FastAPI(debug=True, lifespan=lifespan)
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
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return User(**result)


def get_user_by_username(username: str) -> User:
    result = users_collection.find_one({"username": username})
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return User(**result)


def user_exist(username: str) -> bool:
    return users_collection.find_one({"username": username}) is not None


@app.post("/users/create")
async def post_users_register(session: str, username: str) -> None:
    user = get_user_by_session(session)
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    if user_exist(username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    new_user = User(username=username, password=username)
    users_collection.insert_one(new_user.model_dump())


@app.get("/users/session")
async def get_users_session(username: str, password: str) -> str:
    user = get_user_by_username(username)
    if user.password != password:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    session = str(uuid.uuid4())
    users_collection.update_one(
        {"username": user.username}, {"$push": {"sessions": session}}
    )
    return session


@app.put("/users/password")
async def put_users_password(session: str, username: str, new_password: str) -> None:
    current_user = get_user_by_session(session)
    user_to_update = get_user_by_username(username)
    if not current_user.is_admin and current_user.username != user_to_update.username:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    users_collection.update_one({"username": username}, {"password": new_password})


@app.get("/users/by/session")
async def get_users(session: str) -> UserView:
    user = get_user_by_session(session)
    return UserView(**user.model_dump())


@app.get("/users/by/username")
async def get_users(username: str) -> UserView:
    user = get_user_by_username(username)
    return UserView(**user.model_dump())


@app.post("/tokens/reward")
async def post_tokens_reward(session: str, username: str, value: int) -> None:
    if value <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    current_user = get_user_by_session(session)
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    if not user_exist(username):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

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
                )
            )


@app.post("/tokens/transfer")
async def post_tokens_transfer(session: str, username: str, value: int) -> None:
    if value <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    current_user = get_user_by_session(session)
    if current_user.tokens < value:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    if not user_exist(username):
        raise HTTPException(status.HTTP_404_NOT_FOUND)

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
                )
            )


@app.get("/transactions")
async def get_transactions(
    offset: int = 0, limit: int = 16, initiator: str = None, reciever: str = None
) -> list[Transaction]:
    if offset < 0 or limit <= 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

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
