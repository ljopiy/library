from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.genre import GenreRead
from schemas.series import SeriesRead


class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    published_date: Optional[date] = None
    isbn: Optional[str] = None
    pages: Optional[int] = None
    language: Optional[str] = "ru"
    series_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None


class BookImageCreate(BaseModel):
    url: str
    description: Optional[str] = None


class BookImageRead(BaseModel):
    id: int
    file_path: str
    description: Optional[str]

    class Config:
        orm_mode = True


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    published_date: Optional[date]
    isbn: Optional[str]
    pages: Optional[int]
    language: str
    available: bool
    created_at: datetime
    favorite: bool = False

    series: Optional[SeriesRead]
    genres: List[GenreRead] = []

    images: List[BookImageRead] = []
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    published_date: Optional[date]
    isbn: Optional[str]
    pages: Optional[int]
    language: Optional[str]
    available: Optional[bool]
    series_id: Optional[int]
    genre_ids: Optional[List[int]]
