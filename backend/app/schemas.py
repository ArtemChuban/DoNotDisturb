from pydantic import BaseModel


class TeamInfo(BaseModel):
    id: str
    name: str


class UserInfo(BaseModel):
    username: str
    teams: list[TeamInfo]
    invites: list[TeamInfo]
