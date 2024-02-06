import uuid
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager


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


class User(BaseModel):
    username: str
    password: str
    is_admin: bool = False
    tokens: list[str] = []


def get_user_by_token(token: str) -> User:
    result = users_collection.find_one({"tokens": token})
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
async def post_users_register(token: str, username: str) -> None:
    user = get_user_by_token(token)
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    if user_exist(username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    new_user = User(username=username, password=username)
    users_collection.insert_one(new_user.model_dump())


@app.get("/users/token")
async def get_users_token(username: str, password: str) -> str:
    user = get_user_by_username(username)
    if user.password != password:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    token = str(uuid.uuid4())
    users_collection.update_one(
        {"username": user.username}, {"$push": {"tokens": token}}
    )
    return token


@app.put("/users/password")
async def put_users_password(token: str, username: str, new_password: str) -> None:
    current_user = get_user_by_token(token)
    user_to_update = get_user_by_username(username)
    if not current_user.is_admin and current_user.username != user_to_update.username:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    users_collection.update_one({"username": username}, {"password": new_password})
