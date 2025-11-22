from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from models.series import Series


async def create_series_service(name: str, description: str, db: AsyncSession) -> Series:
    try:
        series = Series(name=name, description=description)
        db.add(series)
        await db.commit()
        await db.refresh(series)
        return series
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Database error while creating series: %s", e)
        raise HTTPException(status_code=500, detail="Database error while creating series")
    except Exception as e:
        logger.exception("Unexpected error while creating series")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {type(e).__name__}")

async def get_series_service(series_id: int, db: AsyncSession):
    result = await db.execute(select(Series).where(Series.id == series_id))
    series = result.scalar_one_or_none()
    if not series:
        raise HTTPException(status_code=404, detail="Серия не найдена")
    return series

async def delete_series_service(series_id: int, db: AsyncSession):
    result = await db.execute(select(Series).where(Series.id == series_id))
    series = result.scalar_one_or_none()
    if not series:
        raise HTTPException(status_code=404, detail="Серия не найдена")
    await db.delete(series)
    await db.commit()
    return series