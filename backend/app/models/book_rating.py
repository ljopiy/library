from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint, Text
from sqlalchemy.orm import relationship
from db.base import Base


class BookRating(Base):
    __tablename__ = "book_ratings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)  # 🔹 комментарий к оценке
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="valid_rating_range"),
    )

    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")
