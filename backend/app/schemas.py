from pydantic import BaseModel


class TeamInfo(BaseModel):
    id: str
    name: str


class UserInfo(BaseModel):
    username: str
    balance: int
    teams: list[TeamInfo]
    invites: list[TeamInfo]


class MemberInfo(BaseModel):
    id: str
    username: str
    is_admin: bool
    tokens: int
