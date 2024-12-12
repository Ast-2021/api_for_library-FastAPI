from pydantic import BaseModel
from datetime import date
from typing import Optional


class Borrow(BaseModel):
    id: int
    book_id: Optional[int] = None
    reader_name: str
    date_of_issue: date
    return_date: Optional[date] = None

    class Config:
        from_attributes = True


class BorrowCreate(BaseModel):
    book_id: int
    reader_name: str


class BorrowUpdate(BaseModel):
    return_date: Optional[date] = None