from enum import Enum

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


class TransactionType(int, Enum):
    REWARD = 0
    TRANSFER = 1


class Transaction(BaseModel):
    from_username: str
    to_username: str
    type: TransactionType
    timestamp: int
    id: str
    value: int
    description: str
