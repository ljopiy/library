from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base


class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    inventory_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(20), default="available")
    book = relationship("Book", back_populates="copies", lazy="joined")

    orders = relationship("Order", secondary="order_copies_association", back_populates="copies")
