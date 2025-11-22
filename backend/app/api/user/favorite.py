from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from db.session import get_session
from schemas.book import BookRead
from services.user_service.favorite_service import add_favorite_service, remove_favorite_service, list_favorites_service

favorites_router = APIRouter(prefix="/favorite")


@favorites_router.post("/{book_id}")
async def add_favorite(book_id: int, current_user: CurrentUser, db: AsyncSession = Depends(get_session)):
    user = await add_favorite_service(current_user.id, book_id, db)
    return {"favorites": [b.id for b in user.favorites]}


@favorites_router.delete("/{book_id}")
async def remove_favorite(book_id: int, current_user: CurrentUser, db: AsyncSession = Depends(get_session)):
    user = await remove_favorite_service(current_user.id, book_id, db)
    return {"favorites": [b.id for b in user.favorites]}


@favorites_router.get("/", response_model=List[BookRead])
async def list_favorites(current_user: CurrentUser, db: AsyncSession = Depends(get_session)):
    books = await list_favorites_service(current_user.id, db)
    return books
