from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException
from core.logging import logger
from models import User, UserRoles


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
