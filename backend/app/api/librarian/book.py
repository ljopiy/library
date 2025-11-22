import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.dependencies import LibrarianUser
from db.session import get_session
from models.book import Book
from schemas.book import BookRead, BookUpdate, BookImageRead, BookCreate
from services.librarian.book_service import update_book_service, delete_book_service, \
    add_book_image_service, delete_book_image_service, get_book_service, create_book_service

librarian_books_router = APIRouter(prefix="/librarian/books", tags=["Librarian Books"])
UPLOAD_DIR = Path("static/uploads")


@librarian_books_router.post("/", response_model=BookRead)
async def create_book(
        data: BookCreate,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Эндпоинт для библиотекарей и админов.
    Создаёт новую книгу.
    """
    return await create_book_service(data, db)


@librarian_books_router.get("/", response_model=List[BookRead])
async def search_books(
        db: AsyncSession = Depends(get_session),
        title: Optional[str] = Query(None, description="Поиск по названию"),
        author: Optional[str] = Query(None, description="Поиск по автору"),
        genre_name: Optional[str] = Query(None, description="Фильтр по жанру (название)"),
        language: Optional[str] = Query(None, description="Фильтр по языку"),
        available: Optional[bool] = Query(None, description="Фильтр по доступности"),
        sort_by: Optional[str] = Query("created_at", description="Поле сортировки"),
        sort_order: Optional[str] = Query("desc", description="asc или desc"),
):
    query = select(Book).options(
        selectinload(Book.genres),
        selectinload(Book.series),
        selectinload(Book.images),
        selectinload(Book.ratings),
    )

    if title:
        query = query.where(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.where(Book.author.ilike(f"%{author}%"))
    if genre_name:
        query = query.join(Book.genres).where(Book.genres.any(name=genre_name))
    if language:
        query = query.where(Book.language == language)
    if available is not None:
        query = query.where(Book.available == available)

    allowed_sorts = {
        "created_at": Book.created_at,
        "title": Book.title,
        "author": Book.author,
        "published_date": Book.published_date,
    }
    sort_column = allowed_sorts.get(sort_by, Book.created_at)

    query = query.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())

    result = await db.execute(query)
    books = result.scalars().all()

    return [
        BookRead.from_orm(book).copy(update={"average_rating": book.calc_average_rating()})
        for book in books
    ]


@librarian_books_router.get("/{book_id}", response_model=BookRead)
async def get_book(
        book_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Получение конкретной книги по ID"""
    return await get_book_service(book_id, db)


@librarian_books_router.put("/{book_id}", response_model=BookRead)
async def update_book(
        book_id: int,
        data: BookUpdate,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Редактирование книги"""
    return await update_book_service(book_id, data, db)


@librarian_books_router.delete("/{book_id}", response_model=BookRead)
async def delete_book(
        book_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Удаление книги"""
    return await delete_book_service(book_id, db)


@librarian_books_router.post("/{book_id}/images", response_model=BookImageRead)
async def upload_book_image(
        book_id: int,
        file: UploadFile,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),

        description: str = ""

):
    """Загрузка картинки для книги"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / unique_name

    with open(file_path, "wb") as f:
        f.write(await file.read())

    url_path = f"/static/uploads/{unique_name}"

    return await add_book_image_service(book_id, url_path, description, db)


@librarian_books_router.delete("/images/{image_id}", response_model=BookImageRead)
async def delete_book_image(
        image_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Удаление картинки книги"""
    return await delete_book_image_service(image_id, db)
