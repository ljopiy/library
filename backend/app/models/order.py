from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from db.base import Base

order_copies_association = Table(
    "order_copies_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("copy_id", Integer, ForeignKey("book_copies.id"), primary_key=True),
)


def default_due_date():
    return datetime.utcnow() + timedelta(days=30)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=default_due_date)
    is_active = Column(Boolean, default=True)
    is_issued = Column(Boolean, default=False)
    issued_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)

    # связи
    user = relationship("User", back_populates="orders")
    copies = relationship(
        "BookCopy",
        secondary=order_copies_association,
        back_populates="orders",
        lazy="selectin"
    )
