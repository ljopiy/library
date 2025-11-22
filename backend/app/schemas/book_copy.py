from pydantic import BaseModel


class BookCopyCreate(BaseModel):
    book_id: int
    inventory_number: str


class BookCopyRead(BaseModel):
    id: int
    book_id: int
    inventory_number: str
    status: str

    class Config:
        orm_mode = True
