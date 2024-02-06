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
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password: str
    is_admin: bool = False
    tokens: list[str] = []


def get_user_by_token(token: str) -> User:
    result = users_collection.find_one({"tokens": token})
    if result is None:
        return None
    return User(**result)


@app.post("/users/create")
async def post_users_register(token: str, username: str) -> None:
    user = get_user_by_token(token)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    if users_collection.find_one({"username": username}) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    new_user = User(username=username, password=username)
    users_collection.insert_one(new_user.model_dump())


@app.get("/users/token")
async def get_users_token(username: str, password: str) -> str:
    user = users_collection.find_one({"username": username, "password": password})
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    user = User(**user)
    token = str(uuid.uuid4())
    users_collection.update_one({"id": user.id}, {"$push": {"tokens": token}})
    return token
