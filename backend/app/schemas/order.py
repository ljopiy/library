from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.book import BookRead


class OrderCreate(BaseModel):
    copy_ids: List[int]


class OrderRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    due_date: datetime
    issued_at: Optional[datetime]
    returned_at: Optional[datetime]
    is_active: bool
    is_issued: bool
    books: List[BookRead] = []

    class Config:
        from_attributes = True

