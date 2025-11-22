from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.book import Book
from models.book_copy import BookCopy


async def create_book_copy_service(book_id: int, inventory_number: str, db: AsyncSession) -> BookCopy:
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    copy = BookCopy(book_id=book_id, inventory_number=inventory_number, status="available")
    db.add(copy)
    await db.commit()
    await db.refresh(copy)
    return copy


async def list_book_copies_service(book_id: int, db: AsyncSession):
    result = await db.execute(select(BookCopy).where(BookCopy.book_id == book_id))
    return result.scalars().all()


async def get_book_copy_service(copy_id: int, db: AsyncSession):
    result = await db.execute(select(BookCopy).where(BookCopy.id == copy_id))
    copy = result.scalar_one_or_none()
    if not copy:
        raise HTTPException(status_code=404, detail="Экземпляр не найден")
    return copy


async def delete_book_copy_service(copy_id: int, db: AsyncSession):
    copy = await get_book_copy_service(copy_id, db)
    await db.delete(copy)
    await db.commit()
    return copy
