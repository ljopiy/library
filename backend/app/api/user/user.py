from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from db.session import get_session
from schemas.change_password import ChangePasswordRequest
from schemas.user import UserRead, AdminUserUpdate
from services.user_service.profile_service import update_profile_service, change_password_service

me_router = APIRouter(prefix="/me", tags=["My Profile"])


@me_router.get("/", response_model=UserRead)
async def get_my_profile(current_user: CurrentUser):
    """
    Получить информацию о самом себе.
    """
    return current_user


@me_router.put("/", response_model=UserRead)
async def update_my_profile(
        update_data: AdminUserUpdate,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    return await update_profile_service(update_data, current_user, db)


@me_router.patch("/password", response_model=UserRead)
async def change_password(
        data: ChangePasswordRequest,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    return await change_password_service(data, current_user, db)
