from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    time: time
    location: str


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class EventRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: date
    time: time
    location: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    creator_id: int

    class Config:
        orm_mode = True
