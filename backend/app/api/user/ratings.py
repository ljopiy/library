from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from db.session import get_session
from schemas.rating import RatingCreate, RatingRead
from services.user_service.rating_service import add_or_update_rating_service, list_ratings_service, \
    delete_rating_service

ratings_router = APIRouter(prefix="/ratings")



@ratings_router.post("/{book_id}", response_model=RatingRead)
async def rate_book(
        book_id: int,
        data: RatingCreate,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    return await add_or_update_rating_service(book_id, current_user.id, data, db)


@ratings_router.get("/{book_id}", response_model=List[RatingRead])
async def list_ratings(book_id: int, db: AsyncSession = Depends(get_session)):
    return await list_ratings_service(book_id, db)


@ratings_router.delete("/{book_id}")
async def delete_rating(book_id: int, current_user: CurrentUser, db: AsyncSession = Depends(get_session)):
    return await delete_rating_service(book_id, current_user.id, db)
