import time

from app.models import Transaction, TransactionType, User
from fastapi import HTTPException, status
from pymongo.collection import Collection


class TokenController:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def transfer(self, initiator: User, username: str, value: int) -> Transaction:
        if value <= 0:
            raise ValueError("Value must be greater then zero")
        if initiator.tokens < value:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "You dont have enough tokens"
            )
        result = self.collection.update_one(
            {"username": username}, {"$inc": {"tokens": value}}
        )
        if result.modified_count != 1:
            raise ValueError("Wrong username")
        result = self.collection.update_one(
            {"username": initiator.username}, {"$inc": {"tokens": -value}}
        )
        if result.modified_count != 1:
            raise ValueError("Wrong initiator")
        return Transaction(
            timestamp=int(time.time()),
            initiator=initiator.username,
            reciever=username,
            value=value,
            type=TransactionType.TRANSFER,
        )

    def reward(self, initiator: User, username: str, value: int) -> Transaction:
        if value <= 0:
            raise ValueError("Value must be greater then zero")
        if not initiator.is_admin:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admin can reward")
        result = self.collection.update_one(
            {"username": username}, {"$inc": {"tokens": value}}
        )
        if result.modified_count != 1:
            raise ValueError("Wrong username")
        return Transaction(
            timestamp=int(time.time()),
            initiator=initiator.username,
            reciever=username,
            value=value,
            type=TransactionType.REWARD,
        )
