from typing import Annotated

import uvicorn
from fastapi import Body, FastAPI, Header
from contextlib import asynccontextmanager
from Controller import Controller
import os


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
    return controller.try_register(username, password)


@app.post("/users/session")
async def post_users_session(
    username: Annotated[str, Body(embed=True)],
    password: Annotated[str, Body(embed=True)],
) -> str:
    return controller.try_login(username, password)


@app.post("/teams")
async def post_team(
    session: Annotated[str, Header()],
    name: Annotated[str, Body(embed=True)],
) -> str:
    return controller.try_create_team(session, name)


@app.post("/teams/invite")
async def post_team_invite(
    session: Annotated[str, Header()],
    team_id: Annotated[str, Body(embed=True)],
    username: Annotated[str, Body(embed=True)],
) -> None:
    controller.try_invite(session, team_id, username)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
