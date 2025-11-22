from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from models.genre import Genre


async def create_genre_service(name: str, db: AsyncSession) -> Genre:
    try:
        genre = Genre(name=name)
        db.add(genre)
        await db.commit()
        await db.refresh(genre)
        return genre
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Database error while creating genre: %s", e)
        raise HTTPException(status_code=500, detail="Database error while creating genre")
    except Exception as e:
        logger.exception("Unexpected error while creating genre")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {type(e).__name__}")

async def get_genre_service(genre_id: int, db: AsyncSession):
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return genre

async def delete_genre_service(genre_id: int, db: AsyncSession):
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    await db.delete(genre)
    await db.commit()
    return genre