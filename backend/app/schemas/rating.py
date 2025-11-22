from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RatingCreate(BaseModel):
    rating: int
    comment: Optional[str] = None

class RatingRead(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
