from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import AdminUserUpdate
from services.user_service.user_service import hash_password


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    result = list(result.scalars().all())
    return result


async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    user: Optional[User] = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user_by_admin(user_id: int, data: AdminUserUpdate, db: AsyncSession) -> User:
    user = await get_user_by_id(user_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def change_user_password_by_admin(user_id: int, new_password: str, db: AsyncSession) -> None:
    user = await get_user_by_id(user_id, db)
    user.hashed_password = hash_password(new_password)
    await db.commit()


async def deactivate_user_by_admin(user_id: int, db: AsyncSession) -> User:
    user = await get_user_by_id(user_id, db)
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return user
