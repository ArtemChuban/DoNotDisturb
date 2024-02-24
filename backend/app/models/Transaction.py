import uuid

from pydantic import BaseModel, Field

from .TransactionType import TransactionType


class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int
    initiator: str
    reciever: str
    value: int
    type: TransactionType
