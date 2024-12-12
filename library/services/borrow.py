from ..models import Borrow, Books
from sqlalchemy.orm import Session
from ..dto import borrow
from fastapi import HTTPException, status


def create_borrow(data: borrow.BorrowCreate, db: Session):
    try:
        borrow = Borrow(book_id=data.book_id, reader_name=data.reader_name)
        book = db.query(Books).filter(Books.id==borrow.book_id).first()
        if book is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={'message': 'book in borrow not found'})
        elif book.available_quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail={'message': 'not available'})
        else:
            book.available_quantity -= 1
            db.add(borrow)
            db.commit()
            db.refresh(borrow)
            return borrow
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        


def get_all_borrow(db: Session):
    borrow = db.query(Borrow).all()
    if borrow:
        return borrow
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


def get_borrow(id: int, db: Session):
    borrow = db.query(Borrow).filter(Borrow.id==id).first()
    if borrow:
        return borrow
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'message': 'borrow not found'})


def update(id: int, data: borrow.BorrowUpdate, db: Session):
    try:
        borrow = get_borrow(id, db)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(borrow, key, value)

        book = db.query(Books).filter(Books.id==borrow.book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={'message': 'book in borrow not found'})
        
        book.available_quantity += 1
        db.commit()
        db.refresh(borrow)
        return borrow

    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'message': 'Borrow data could not be updated'})



def remove(id: int, db: Session):
    borrow = db.query(Borrow).filter(Borrow.id==id).first()
    if not borrow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'message': 'borrow not found'})
    try:
        db.delete(borrow)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    except Exception :
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)