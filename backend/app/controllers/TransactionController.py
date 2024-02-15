from typing import Optional

from app.models import Transaction
from pymongo.collection import Collection


class TransactionController:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def add(self, transaction: Transaction) -> None:
        self.collection.insert_one(transaction.model_dump())

    def get(
        self,
        offset: int = 0,
        limit: int = 8,
        initiator: Optional[str] = None,
        reciever: Optional[str] = None,
    ) -> list[Transaction]:
        query = {}
        if initiator:
            query["initiator"] = initiator
        if reciever:
            query["reciever"] = reciever
        transactions = (
            self.collection.find(query).sort("timestamp", -1).skip(offset).limit(limit)
        )
        return [Transaction(**transaction) for transaction in transactions]
