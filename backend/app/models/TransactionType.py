from enum import Enum


class TransactionType(str, Enum):
    TRANSFER = "Transfer"
    REWARD = "Reward"
