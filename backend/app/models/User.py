from . import UserView


class User(UserView):
    password: str
    sessions: list[str] = []
