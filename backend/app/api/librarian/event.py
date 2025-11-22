from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser
from db.session import get_session
from schemas.events import EventCreate, EventRead, EventUpdate
from services.librarian.event_service import (
    create_event_service,
    update_event_service,
    delete_event_service,
    list_events_service,
    get_event_service,
)

events_router = APIRouter(prefix="/events", tags=["Events"])


@events_router.post("/", response_model=EventRead)
async def create_event(
        data: EventCreate,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    return await create_event_service(data, current_user.id, db)


@events_router.put("/{event_id}", response_model=EventRead)
async def update_event(
        event_id: int,
        data: EventUpdate,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    return await update_event_service(event_id, data, current_user.id, db)


@events_router.delete("/{event_id}")
async def delete_event(
        event_id: int,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    return await delete_event_service(event_id, current_user.id, db)


@events_router.get("/", response_model=List[EventRead])
async def list_events(db: AsyncSession = Depends(get_session)):
    return await list_events_service(db)


@events_router.get("/{event_id}", response_model=EventRead)
async def get_event(event_id: int, db: AsyncSession = Depends(get_session)):
    return await get_event_service(event_id, db)
