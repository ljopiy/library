from sqlalchemy import Table, Column, Integer, ForeignKey
from db.base import Base

user_favorites = Table(
    "user_favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
)
