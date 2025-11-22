from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base
from models.book import book_genre_association


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    books = relationship("Book", secondary=book_genre_association, back_populates="genres")
