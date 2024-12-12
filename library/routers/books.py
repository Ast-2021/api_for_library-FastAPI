from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

from ..services import books as BookService
from ..dto import books as BookDTO


router = APIRouter()


@router.post('/', tags=['books'], response_model=BookDTO.BookCreate)
async def create(data: BookDTO.BookCreate, db: Session=Depends(get_db)):
    book = BookService.create_book(data, db)
    return book


@router.get('/', tags=['books'], response_model=List[BookDTO.Book])
async def get_books(db: Session = Depends(get_db)):
    books = BookService.get_all_books(db)
    return books


@router.get('/{id}', tags=['books'], response_model=BookDTO.Book)
async def get(id: int, db: Session=Depends(get_db)):
    book =  BookService.get_book(id, db)
    return book


@router.put('/{id}', tags=['books'], response_model=BookDTO.BookUpdate)
async def update(id: int, data: BookDTO.BookUpdate, db: Session=Depends(get_db)):
    book = BookService.update(id, data, db)
    return book


@router.delete('/{id}', tags=['books'], status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session=Depends(get_db)):
    book =  BookService.remove(id, db)
    return book