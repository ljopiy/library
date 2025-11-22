from pydantic import BaseModel

from models.users_roles import UserRoles


class Token(BaseModel):
    access_token: str
    token_type: str
    user_role: str


class TokenData(BaseModel):
    sub: str | None = None
    role: UserRoles | None = None
