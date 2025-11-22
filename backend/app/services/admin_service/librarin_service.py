from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from models import User, UserRoles
from services.user_service.user_service import get_user_by_id


async def list_librarians_service(db: AsyncSession):
    """
    Возвращает список всех библиотекарей.
    """
    try:
        result = await db.execute(
            select(User).where(User.role == UserRoles.LIBRARIAN)
        )
        librarians = result.scalars().all()
        return librarians

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Database error while fetching librarians: %s", e)
        raise HTTPException(status_code=500, detail="Database error while fetching librarians")

    except Exception as e:
        logger.exception("Unexpected error while fetching librarians")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {type(e).__name__}")


async def get_librarian_service(user_id: int, db: AsyncSession):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user.role != UserRoles.LIBRARIAN:
        raise HTTPException(status_code=403, detail="Это не библиотекарь")

    return user
