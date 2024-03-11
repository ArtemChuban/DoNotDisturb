from typing import Annotated

import uvicorn
from fastapi import Body, FastAPI
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
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
) -> str:
    return controller.try_register(username, password)


@app.post("/users/session")
async def post_users_session(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
) -> str:
    return controller.try_login(username, password)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
