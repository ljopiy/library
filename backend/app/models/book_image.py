from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class BookImage(Base):
    __tablename__ = "book_images"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(500), nullable=False)  # путь к файлу на сервере
    description = Column(String(255), nullable=True)

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    book = relationship("Book", back_populates="images")