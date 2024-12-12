from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class Author(BaseModel):
    id: int
    name: str 
    last_name: str
    date_of_birth: date

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя должно быть от 2 до 50 символов") 
    last_name: str = Field(..., min_length=2, max_length=50, description="Фамилия должна быть от 2 до 50 символов")
    date_of_birth: date

class AuthorUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя должно быть от 2 до 50 символов") 
    last_name: str = Field(..., min_length=2, max_length=50, description="Фамилия должна быть от 2 до 50 символов")
    date_of_birth: date