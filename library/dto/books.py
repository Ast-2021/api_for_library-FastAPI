from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    description: str
    author_id: Optional[int] = None
    available_quantity: int

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    description: str
    author_id: int

class BookUpdate(BaseModel):
    title: str
    description: str
    author_id: Optional[int] = None