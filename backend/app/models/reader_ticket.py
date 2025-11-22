from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .index import Base


class ReaderTicket(Base):
    __tablename__ = "reader_ticket"

    ticket_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", back_populates="ticket", uselist=False)