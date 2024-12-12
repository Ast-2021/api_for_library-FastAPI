from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    description: str
    author_id: Optional[int] = None
    available_quantity: int

    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=50, description="Название книги должно быть от 2 до 50 символов") 
    description: str = Field(..., min_length=30, max_length=3000, description="Описание книги должно быть от 30 до 3000 символов")
    author_id: int 
    available_quantity: Optional[int] = 10

class BookUpdate(BaseModel):
    title: str = Field(..., min_length=2, max_length=50, description="Название книги должно быть от 2 до 50 символов")
    description: str = Field(..., min_length=30, max_length=3000, description="Описание книги должно быть от 30 до 3000 символов")
    author_id: Optional[int] = None