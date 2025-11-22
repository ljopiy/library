from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.logging import logger
from models.book import Book
from models.book_image import BookImage
from models.genre import Genre
from schemas.book import BookCreate, BookUpdate


async def create_book_service(data: BookCreate, db: AsyncSession) -> Book:
    try:
        if data.isbn:
            result = await db.execute(select(Book).where(Book.isbn == data.isbn))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")

        book = Book(
            title=data.title,
            author=data.author,
            description=data.description,
            published_date=data.published_date,
            isbn=data.isbn,
            pages=data.pages,
            language=data.language,
            series_id=data.series_id,
        )

        if data.genre_ids:
            result = await db.execute(select(Genre).where(Genre.id.in_(data.genre_ids)))
            genres = result.scalars().all()
            book.genres = genres

        db.add(book)
        await db.commit()
        await db.refresh(book)

        return book

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Database error while creating book: %s", e)
        raise HTTPException(status_code=500, detail="Database error while creating book")
    except Exception as e:
        logger.exception("Unexpected error while creating book")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {type(e).__name__}")


async def get_all_books_service(db: AsyncSession):
    result = await db.execute(
        select(Book).options(
            selectinload(Book.genres),
            selectinload(Book.series),
            selectinload(Book.images)
        )
    )
    return result.scalars().all()


async def update_book_service(book_id: int, data: BookUpdate, db: AsyncSession):
    try:
        result = await db.execute(
            select(Book).options(selectinload(Book.genres), selectinload(Book.series)).where(Book.id == book_id)
        )
        book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")

        for field, value in data.dict(exclude_unset=True).items():
            if field == "genre_ids":
                genres = await db.execute(select(Genre).where(Genre.id.in_(value)))
                book.genres = genres.scalars().all()
            else:
                setattr(book, field, value)

        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Ошибка при редактировании книги: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при редактировании книги")


async def delete_book_service(book_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена")

        await db.delete(book)
        await db.commit()
        return book
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Ошибка при удалении книги: %s", e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении книги")


async def add_book_image_service(book_id: int, file_path: str, description: str, db: AsyncSession):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    image = BookImage(file_path=file_path, description=description, book=book)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def delete_book_image_service(image_id: int, db: AsyncSession):
    result = await db.execute(select(BookImage).where(BookImage.id == image_id))
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Картинка не найдена")

    try:
        import os
        if os.path.exists(image.file_path.replace("/static/", "static/")):
            os.remove(image.file_path.replace("/static/", "static/"))
    except Exception:
        pass

    await db.delete(image)
    await db.commit()
    return


async def get_book_service(book_id: int, db: AsyncSession):
    result = await db.execute(
        select(Book).options(
            selectinload(Book.genres),
            selectinload(Book.series),
            selectinload(Book.images)
        ).where(Book.id == book_id)
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book
