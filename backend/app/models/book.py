from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from db.base import Base

book_genre_association = Table(
    "book_genre_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    published_date = Column(Date, nullable=True)
    isbn = Column(String(13), unique=True, nullable=True)
    pages = Column(Integer, nullable=True)
    language = Column(String(50), default="ru")
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship(
        "BookImage",
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    series_id = Column(Integer, ForeignKey("series.id"), nullable=True)
    series = relationship(
        "Series",
        back_populates="books",
        lazy="joined"
    )

    genres = relationship(
        "Genre",
        secondary=book_genre_association,
        back_populates="books",
        lazy="selectin"
    )

    # 🔹 удобное свойство для сериализации
    @property
    def genre_ids(self):
        return [genre.id for genre in self.genres]
