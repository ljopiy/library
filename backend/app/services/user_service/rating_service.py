from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from models.book_rating import BookRating
from schemas.rating import RatingCreate

async def add_or_update_rating_service(book_id: int, user_id: int, data: RatingCreate, db: AsyncSession) -> BookRating:
    # Проверяем, есть ли уже оценка от этого пользователя
    result = await db.execute(
        select(BookRating).where(BookRating.book_id == book_id, BookRating.user_id == user_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.rating = data.rating
        existing.comment = data.comment
    else:
        new_rating = BookRating(book_id=book_id, user_id=user_id, rating=data.rating, comment=data.comment)
        db.add(new_rating)

    await db.commit()
    return existing or new_rating


async def list_ratings_service(book_id: int, db: AsyncSession):
    result = await db.execute(select(BookRating).where(BookRating.book_id == book_id))
    return result.scalars().all()


async def delete_rating_service(book_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(
        select(BookRating).where(BookRating.book_id == book_id, BookRating.user_id == user_id)
    )
    rating = result.scalar_one_or_none()
    if not rating:
        raise HTTPException(status_code=404, detail="Оценка не найдена")

    await db.delete(rating)
    await db.commit()
    return {"detail": "Оценка удалена"}
