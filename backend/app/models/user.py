from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .index import Base
from .users_roles import UserRoles


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticket_id: Mapped[str] = mapped_column(ForeignKey("reader_ticket.ticket_id"))
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), nullable=False, default=UserRoles.USER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan", lazy="selectin")

    ticket = relationship("ReaderTicket", back_populates="user")
