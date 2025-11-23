from typing import Optional

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

from ai_model import recommender_model


class UserRecommendationsRequest(BaseModel):
    user_id: int
    n_personal: Optional[int] = 5


class BookSimilarRequest(BaseModel):
    book_id: int
    n_similar: Optional[int] = 5


recommendation_router = APIRouter(prefix="/user/recommendation")


@recommendation_router.get("/recommendations/{user_id}")
def get_personal_recommendations(user_id: int, n: int = 5):
    recommendations = recommender_model.recommend_books_personalized(user_id, n)
    if not recommendations:
        raise HTTPException(status_code=404, detail="User not found or no recommendations available")
    return {"user_id": user_id, "recommendations": recommendations}


@recommendation_router.get("/similar_books/{book_id}")
def get_similar_books(book_id: int, n: int = 5):
    similar_books = recommender_model.get_similar_books_personalized(book_id, n)
    if not similar_books:
        raise HTTPException(status_code=404, detail="Book not found or no similar books available")
    return {"book_id": book_id, "similar_books": similar_books}
