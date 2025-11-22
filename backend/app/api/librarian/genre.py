from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import LibrarianUser
from db.session import get_session
from schemas.genre import GenreCreate, GenreRead
from schemas.series import SeriesCreate, SeriesRead
from services.librarian.genre_service import create_genre_service, delete_genre_service, get_genre_service
from services.librarian.series_service import create_series_service, get_series_service, delete_series_service

librarian_genres_series_router = APIRouter(prefix="/librarian")


@librarian_genres_series_router.post("/genres", response_model=GenreRead)
async def create_genre(
        data: GenreCreate,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Создание нового жанра (библиотекарь или админ).
    """
    return await create_genre_service(data.name, db)


@librarian_genres_series_router.post("/series", response_model=SeriesRead)
async def create_series(
        data: SeriesCreate,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """
    Создание новой серии книг (библиотекарь или админ).
    """
    return await create_series_service(data.name, data.description, db)


@librarian_genres_series_router.get("/genres/{genre_id}", response_model=GenreRead)
async def get_genre(
        genre_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Получение конкретного жанра"""
    return await get_genre_service(genre_id, db)


@librarian_genres_series_router.delete("/genres/{genre_id}", response_model=GenreRead)
async def delete_genre(
        genre_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Удаление жанра"""
    return await delete_genre_service(genre_id, db)


@librarian_genres_series_router.get("/series/{series_id}", response_model=SeriesRead)
async def get_series(
        series_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Получение конкретной серии"""
    return await get_series_service(series_id, db)


@librarian_genres_series_router.delete("/series/{series_id}", response_model=SeriesRead)
async def delete_series(
        series_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    """Удаление серии"""
    return await delete_series_service(series_id, db)
