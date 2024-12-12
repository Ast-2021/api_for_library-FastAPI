from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

from ..services import authors as AuthorService
from ..dto import authors as AuthorDTO


router = APIRouter()


@router.post('/', tags=['authors'], response_model=AuthorDTO.AuthorCreate)
async def create(data: AuthorDTO.AuthorCreate, db: Session=Depends(get_db)):
    author = AuthorService.create_author(data, db)
    return author




@router.get('/', tags=['authors'], response_model=List[AuthorDTO.Author])
async def get_authors(db: Session = Depends(get_db)):
    authors = AuthorService.get_all_authors(db)
    return authors


@router.get('/{id}', tags=['authors'], response_model=AuthorDTO.Author)
async def get(id: int, db: Session=Depends(get_db)):
    author =  AuthorService.get_author(id, db)
    return author


@router.put('/{id}', tags=['authors'], response_model=AuthorDTO.AuthorUpdate)
async def update(id: int, data: AuthorDTO.AuthorUpdate, db: Session=Depends(get_db)):
    author = AuthorService.update(id, data, db)
    return author


@router.delete('/{id}', tags=['authors'], status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session=Depends(get_db)):
    AuthorService.remove(id, db)
