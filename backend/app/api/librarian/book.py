import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import LibrarianUser, CurrentUser
from db.session import get_session
from schemas.book import BookCreate, BookRead, BookUpdate, BookImageRead
from services.librarian.book_service import create_book_service, update_book_service, delete_book_service, \
    get_all_books_service, add_book_image_service, delete_book_image_service, get_book_service

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
async def get_all_books(
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    """Получение списка всех книг"""
    return await get_all_books_service(db)


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
