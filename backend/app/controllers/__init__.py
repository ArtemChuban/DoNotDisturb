from app.database import transactions_collection, users_collection

from .TransactionController import TransactionController
from .UserController import UserController
from .TokenController import TokenController

user_controller = UserController(users_collection)
transaction_controller = TransactionController(transactions_collection)
token_controller = TokenController(users_collection)
