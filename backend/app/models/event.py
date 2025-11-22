from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    location = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    creator = relationship("User", back_populates="created_events")
