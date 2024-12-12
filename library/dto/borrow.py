from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional


class Borrow(BaseModel):
    id: int
    book_id: Optional[int] = None
    reader_name: str
    date_of_issue: date
    return_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class BorrowCreate(BaseModel):
    book_id: int
    reader_name: str = Field(..., min_length=2, max_length=50, description="Имя читателя должно быть от 2 до 50 символов")


class BorrowUpdate(BaseModel):
    return_date: Optional[date] = None