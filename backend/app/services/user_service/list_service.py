from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


async def list_users_service(db: AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await db.execute(stmt)
    return result.scalars().all()
