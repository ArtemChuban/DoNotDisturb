import os
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from Controller import Controller
from fastapi import Body, FastAPI, Header
from schemas import UserInfo


@asynccontextmanager
async def lifespan(app: FastAPI):
    controller.start()
    yield
    controller.stop()


app = FastAPI(debug=True, lifespan=lifespan)
controller = Controller()


@app.post("/users")
async def post_users(
    username: Annotated[str, Body(embed=True)],
    password: Annotated[str, Body(embed=True)],
) -> str:
    return controller.register(username, password)


@app.post("/users/session")
async def post_users_session(
    username: Annotated[str, Body(embed=True)],
    password: Annotated[str, Body(embed=True)],
) -> str:
    return controller.login(username, password)


@app.post("/teams")
async def post_team(
    session: Annotated[str, Header()],
    name: Annotated[str, Body(embed=True)],
) -> str:
    return controller.create_team(session, name)


@app.post("/teams/invite")
async def post_team_invite(
    session: Annotated[str, Header()],
    team_id: Annotated[str, Body(embed=True)],
    username: Annotated[str, Body(embed=True)],
) -> None:
    controller.invite(session, team_id, username)


@app.post("/teams/invite/reply")
async def post_teams_invite_reply(
    session: Annotated[str, Header()],
    team_id: Annotated[str, Body(embed=True)],
    accepted: Annotated[bool, Body(embed=True)],
):
    controller.invite_reply(session, team_id, accepted)


@app.post("/reward")
async def post_reward(
    session: Annotated[str, Header()],
    team_id: Annotated[str, Body(embed=True)],
    user_id: Annotated[str, Body(embed=True)],
    value: Annotated[int, Body(embed=True, gt=0)],
):
    controller.reward(session, team_id, user_id, value)


@app.post("/transfer")
async def post_transfer(
    session: Annotated[str, Header()],
    team_id: Annotated[str, Body(embed=True)],
    user_id: Annotated[str, Body(embed=True)],
    value: Annotated[int, Body(embed=True, gt=0)],
):
    controller.transfer(session, team_id, user_id, value)


@app.get("/users")
async def get_users(
    session: Annotated[str, Header()],
) -> UserInfo:
    return controller.get_user(session)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
