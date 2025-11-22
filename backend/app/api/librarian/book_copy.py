from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import LibrarianUser
from db.session import get_session
from schemas.book_copy import BookCopyCreate, BookCopyRead
from services.librarian.book_copy_service import (
    create_book_copy_service,
    list_book_copies_service,
    get_book_copy_service,
    delete_book_copy_service,
)

book_copy_router = APIRouter(prefix="/librarian/book_copies", tags=["Book Copies"])


@book_copy_router.post("/", response_model=BookCopyRead)
async def create_book_copy(
        data: BookCopyCreate,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Создание экземпляра книги"""
    return await create_book_copy_service(data.book_id, data.inventory_number, db)


@book_copy_router.get("/book/{book_id}", response_model=list[BookCopyRead])
async def list_book_copies(
        book_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Список экземпляров книги"""
    return await list_book_copies_service(book_id, db)


@book_copy_router.get("/{copy_id}", response_model=BookCopyRead)
async def get_book_copy(
        copy_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Получение конкретного экземпляра"""
    return await get_book_copy_service(copy_id, db)


@book_copy_router.delete("/{copy_id}", response_model=BookCopyRead)
async def delete_book_copy(
        copy_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Удаление экземпляра книги"""
    return await delete_book_copy_service(copy_id, db)
