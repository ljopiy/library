from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import AdminUser
from core.logging import logger
from db.session import get_session
from models import UserRoles
from schemas.user import UserRegisterResponse, UserRead, AdminUserUpdate
from services.admin_service.librarin_service import list_librarians_service, get_librarian_service
from services.user_service.user_service import create_user, get_user_by_id

admin_librarian_router = APIRouter(prefix="/admin/librarians")


@admin_librarian_router.post("/register", response_model=UserRegisterResponse)
async def register_librarian(
        current_user: AdminUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Эндпоинт для админа.
    Регистрирует нового библиотекаря.
    """
    try:
        user, raw_password = await create_user(db, role=UserRoles.LIBRARIAN)

        return UserRegisterResponse(
            id=user.id,
            ticket_id=user.ticket_id,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            password=raw_password,
        )
    except Exception as e:
        logger.error(f"Ошибка при регистрации библиотекаря: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании библиотекаря")


@admin_librarian_router.put("/{user_id}", response_model=UserRead)
async def update_librarian(
        user_id: int,
        update_data: AdminUserUpdate,
        current_user: AdminUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Эндпоинт для админа.
    Позволяет редактировать библиотекарей, но не админов.
    """
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if user.role == UserRoles.ADMIN:
            raise HTTPException(status_code=403, detail="Нельзя редактировать админов")

        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.role is not None:
            user.role = update_data.role
        if update_data.is_active is not None:
            user.is_active = update_data.is_active

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при редактировании библиотекаря: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при редактировании библиотекаря")


@admin_librarian_router.delete("/{user_id}", response_model=UserRead)
async def delete_librarian(
        user_id: int,
        current_user: AdminUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Эндпоинт для админа.
    Удаляет библиотекаря, но не админа.
    """
    try:
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if user.role == UserRoles.ADMIN:
            raise HTTPException(status_code=403, detail="Нельзя удалять админов")

        await db.delete(user)
        await db.commit()

        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при удалении библиотекаря: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при удалении библиотекаря")


@admin_librarian_router.get("/", response_model=List[UserRead])
async def list_librarians(
        current_user: AdminUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Эндпоинт для админа.
    Возвращает список всех библиотекарей.
    """
    return await list_librarians_service(db)


@admin_librarian_router.get("/{user_id}", response_model=UserRead)
async def get_librarian(
        user_id: int,
        current_user: AdminUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Эндпоинт для админа.
    Возвращает конкретного библиотекаря по ID.
    """
    return await get_librarian_service(user_id, db)
