from pydantic import BaseModel
from datetime import date


class Author(BaseModel):
    id: int
    name: str
    last_name: str
    date_of_birth: date

    class Config:
        from_attributes = True


class AuthorCreate(BaseModel):
    name: str
    last_name: str
    date_of_birth: date

class AuthorUpdate(BaseModel):
    name: str
    last_name: str
    date_of_birth: date