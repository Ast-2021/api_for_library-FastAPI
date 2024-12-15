from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

from ..services import borrow as BorrowService
from ..dto import borrow as BorrowDTO


router = APIRouter()


@router.post('/', tags=['borrow'], response_model=BorrowDTO.Borrow)
async def create(data: BorrowDTO.BorrowCreate, db: Session=Depends(get_db)):
    borrow = BorrowService.create_borrow(data, db)
    return borrow


@router.get('/', tags=['borrow'], response_model=List[BorrowDTO.Borrow])
async def get_borrows(db: Session = Depends(get_db)):
    borrow = BorrowService.get_all_borrow(db)
    return borrow


@router.get('/{id}', tags=['borrow'], response_model=BorrowDTO.Borrow)
async def get(id: int, db: Session=Depends(get_db)):
    borrow =  BorrowService.get_borrow(id, db)
    return borrow


@router.patch('/{id}', tags=['borrow'], response_model=BorrowDTO.BorrowUpdate)
async def update(id: int, data: BorrowDTO.BorrowUpdate, db: Session=Depends(get_db)):
    borrow = BorrowService.update(id, data, db)
    return borrow


@router.delete('/{id}', tags=['borrow'], status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session=Depends(get_db)):
    borrow =  BorrowService.remove(id, db)
    return borrow