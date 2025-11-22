from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import LibrarianUser
from core.logging import logger
from db.session import get_session
from models import UserRoles
from schemas.user import UserRegisterResponse, UserCreateByLibrarian, UserRead, AdminUserUpdate
from services.user_service.list_service import list_users_service
from services.user_service.profile_service import update_profile_service
from services.user_service.user_service import create_user, get_user_by_id, get_user_service

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


librarian_user_router = APIRouter(prefix="/admin/users", tags=["Librarian Users"])


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


@librarian_user_router.put("/{user_id}", response_model=UserRead)
async def update_user_by_librarian(
        user_id: int,
        update_data: AdminUserUpdate,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Библиотекарь / админ может менять данные только у пользователей с ролью USER.
    """
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if user.role in (UserRoles.ADMIN, UserRoles.LIBRARIAN):
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав для редактирования администраторов или библиотекарей",
            )

        updated_user = await update_profile_service(
            update_data=update_data,
            current_user=user,
            db=db,
        )

        return updated_user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при редактировании пользователя библиотекарем: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при редактировании пользователя")


@librarian_user_router.get("/", response_model=list[UserRead])
async def get_users_list(
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Получение полного списка пользователей.
    Доступно библиотекарям и администраторам.
    """
    try:
        users = await list_users_service(db)
        return users

    except Exception as e:
        logger.error(f"Ошибка при получении списка пользователей: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении списка пользователей")


@librarian_user_router.get("/{user_id}", response_model=UserRead)
async def get_user(
        user_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Получение конкретного пользователя по ID.
    Доступно библиотекарям и администраторам.
    """
    return await get_user_service(user_id, db)
