from pydantic import BaseModel


class UserView(BaseModel):
    username: str
    is_admin: bool = False
    tokens: int = 0
    locale: str = "en"
