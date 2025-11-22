from datetime import datetime
from random import randint

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from core.security import hash_password, verify_password, generate_password
from models.reader_ticket import ReaderTicket
from models.user import User
from models.users_roles import UserRoles


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Получить пользователя по его ID.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


def generate_ticket_id() -> str:
    """Генерация случайного 8-значного номера (только цифры)."""
    return str(randint(10_000_000, 99_999_999))


async def create_user(
        db: AsyncSession,
        role: UserRoles = UserRoles.USER,
        email: str | None = None
) -> tuple[User, str]:
    try:
        for _ in range(5):
            ticket_id = generate_ticket_id()
            existing = await db.execute(select(ReaderTicket).where(ReaderTicket.ticket_id == ticket_id))
            if existing.scalar_one_or_none() is None:
                break
        else:
            raise RuntimeError("Не удалось сгенерировать уникальный ticket_id")

        ticket = ReaderTicket(ticket_id=ticket_id, issued_at=datetime.now(), is_active=True)
        db.add(ticket)

        raw_password = generate_password()
        user = User(
            ticket_id=ticket_id,
            email=email,
            hashed_password=hash_password(raw_password),
            role=role,
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user, raw_password
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("DB error creating user: %s", e)
        raise RuntimeError("Database error") from e


async def authenticate_user_by_ticket(db: AsyncSession, ticket_id: str, password: str) -> User | None:
    result = await db.execute(select(User).where(User.ticket_id == ticket_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user
