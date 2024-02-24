from .UserView import UserView


class User(UserView):
    password: str
    sessions: list[str] = []
