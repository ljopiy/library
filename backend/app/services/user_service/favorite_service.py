from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from models.book import Book


async def add_favorite_service(user_id: int, book_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    book = await db.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    user.favorites.append(book)
    await db.commit()
    await db.refresh(user)
    return user


async def remove_favorite_service(user_id: int, book_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    book = await db.get(Book, book_id)

    if book in user.favorites:
        user.favorites.remove(book)
        await db.commit()
        await db.refresh(user)
    return user


async def list_favorites_service(user_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    return user.favorites
