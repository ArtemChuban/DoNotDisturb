import os
from contextlib import asynccontextmanager
from typing import Annotated

from app.controllers import transaction_controller, user_controller, token_controller
from app.database import mongoClient
from app.models import Transaction, UserView
from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    user_controller.check_admin_exist()
    yield
    # Shutdown
    ...


app = FastAPI(debug=os.environ["MODE"] == "local", lifespan=lifespan, root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def get_root() -> RedirectResponse:
    return RedirectResponse("/api/docs")


@app.post("/users/create")
async def post_users_register(
    session: str, username: Annotated[str, Query(min_length=1)], password: str
) -> None:
    user_controller.create(session, username, password)


@app.put("/users/locale")
async def put_users_locale(session: str, locale: str) -> None:
    user_controller.update_locale(session, locale)


@app.get("/users")
async def get_users() -> list[UserView]:
    return user_controller.get_all()


@app.get("/users/session")
async def get_users_session(username: str, password: str) -> str:
    return user_controller.generate_session(username, password)


@app.put("/users/password")
async def put_users_password(session: str, username: str, new_password: str) -> None:
    user_controller.update_password(session, username, new_password)


@app.get("/users/by/session")
async def get_users_by_session(session: str) -> UserView:
    return UserView(**user_controller.get_by_session(session).model_dump())


@app.get("/users/by/username")
async def get_users_by_username(username: str) -> UserView:
    return UserView(**user_controller.get_by_username(username).model_dump())


@app.post("/tokens/reward")
async def post_tokens_reward(
    session: str, username: str, value: Annotated[int, Query(gt=0)]
) -> None:
    initiator = user_controller.get_by_session(session)
    if not user_controller.username_exist(username):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "User with this username not found"
        )
    with mongoClient.start_session() as mongoSession:
        with mongoSession.start_transaction():
            transaction = token_controller.reward(initiator, username, value)
            transaction_controller.add(transaction)


@app.post("/tokens/transfer")
async def post_tokens_transfer(
    session: str, username: str, value: Annotated[int, Query(gt=0)]
) -> None:
    initiator = user_controller.get_by_session(session)
    if not user_controller.username_exist(username):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "User with this username not found"
        )
    with mongoClient.start_session() as mongoSession:
        with mongoSession.start_transaction():
            transaction = token_controller.transfer(initiator, username, value)
            transaction_controller.add(transaction)


@app.get("/transactions")
async def get_transactions(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0)] = 8,
    initiator: str = None,
    reciever: str = None,
) -> list[Transaction]:
    return transaction_controller.get(offset, limit, initiator, reciever)
