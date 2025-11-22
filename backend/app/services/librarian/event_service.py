from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.event import Event
from schemas.events import EventUpdate, EventCreate


async def update_event_service(event_id: int, data: EventUpdate, user_id: int, db: AsyncSession) -> Event:
    result = await db.execute(select(Event).where(Event.id == event_id, Event.creator_id == user_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено или нет прав на редактирование")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(event, field, value)

    await db.commit()
    await db.refresh(event)
    return event


async def delete_event_service(event_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(select(Event).where(Event.id == event_id, Event.creator_id == user_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено или нет прав на удаление")

    await db.delete(event)
    await db.commit()
    return {"detail": "Мероприятие удалено"}


async def create_event_service(data: EventCreate, user_id: int, db: AsyncSession) -> Event:
    event = Event(**data.dict(), creator_id=user_id)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

async def list_events_service(db: AsyncSession):
    result = await db.execute(select(Event))
    return result.scalars().all()

async def get_event_service(event_id: int, db: AsyncSession) -> Event:
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Мероприятие не найдено")
    return event