from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr

from models import UserRoles


class RegisterUserRequest(BaseModel):
    role: UserRoles


class UserRegisterResponse(BaseModel):
    id: int
    ticket_id: str
    role: UserRoles
    is_active: bool
    created_at: datetime
    password: str

    class Config:
        from_attributes = True


class UserCreateByLibrarian(BaseModel):
    """
    Схема для регистрации пользователя библиотекарем.
    Персональные данные не хранятся, только роль.
    """
    role: UserRoles = UserRoles.USER


class UserLogin(BaseModel):
    """
    Схема для входа пользователя по билету.
    """
    ticket_id: str
    password: str


class UserRead(BaseModel):
    """
    Схема для возврата информации о пользователе.
    """
    id: int
    ticket_id: str
    role: UserRoles
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class AdminUserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRoles] = None
    is_active: Optional[bool] = None
