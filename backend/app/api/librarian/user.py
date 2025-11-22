from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import LibrarianUser
from core.logging import logger
from db.session import get_session
from schemas.user import UserRegisterResponse, UserCreateByLibrarian
from services.user_service.user_service import create_user

librarian_user_router = APIRouter(prefix="/admin/users")


@librarian_user_router.post("/register", response_model=UserRegisterResponse)
async def register_user_by_librarian(
        data: UserCreateByLibrarian,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Эндпоинт для библиотекарей и админов.
    Регистрирует нового пользователя с ролью USER (или указанной).
    """
    try:
        user, raw_password = await create_user(db, role=data.role)

        return UserRegisterResponse(
            id=user.id,
            ticket_id=user.ticket_id,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            password=raw_password,
        )
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя библиотекарем: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании пользователя")
