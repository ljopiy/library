from fastapi import APIRouter

from api.dependencies import AdminUser
from schemas.user import UserRead

admin_user_router = APIRouter(prefix="/admin/users")


@admin_user_router.get("/me", response_model=UserRead)
async def read_users_me(current_user: AdminUser):
    return current_user
