from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

from ..services import authors as AuthorService
from ..dto import authors as AuthorDTO


router = APIRouter()


@router.post('/', tags=['authors'], response_model=AuthorDTO.AuthorCreate)
async def create(data: AuthorDTO.AuthorCreate, db: Session=Depends(get_db)):
    author = AuthorService.create_author(data, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating author")
    return author


@router.get('/', tags=['authors'], response_model=List[AuthorDTO.Author])
async def get_authors(db: Session = Depends(get_db)):
    authors = AuthorService.get_all_authors(db)
    return authors


@router.get('/{id}', tags=['authors'], response_model=AuthorDTO.Author)
async def get(id: int, db: Session=Depends(get_db)):
    author =  AuthorService.get_author(id, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.put('/{id}', tags=['authors'], response_model=AuthorDTO.AuthorUpdate)
async def update(id: int, data: AuthorDTO.AuthorUpdate, db: Session=Depends(get_db)):
    author = AuthorService.update(id, data, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.delete('/{id}', tags=['authors'], status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session=Depends(get_db)):
    author =  AuthorService.remove(id, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author