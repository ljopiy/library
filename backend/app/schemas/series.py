from typing import Optional

from pydantic import BaseModel


class SeriesCreate(BaseModel):
    name: str
    description: Optional[str] = None


class SeriesRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
