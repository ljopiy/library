from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    books = relationship("Book", back_populates="series")
