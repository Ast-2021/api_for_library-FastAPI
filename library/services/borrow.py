from ..models import Borrow
from sqlalchemy.orm import Session
from ..dto import borrow


def create_borrow(data: borrow.BorrowCreate, db):
    borrow = Borrow(book_id=data.book_id, reader_name=data.reader_name)
    try:
        db.add(borrow)
        db.commit()
        db.refresh(borrow)
    except Exception as error:
        db.rollback()
        print(error)
        return None
    
    return borrow


def get_all_borrow(db: Session):
    try:
        borrow = db.query(Borrow).all()
        return borrow
    except Exception as error:
        print(error)
        return None


def get_borrow(id: int, db):
    try:
        return db.query(Borrow).filter(Borrow.id==id).first()
    except Exception as error:
        print(error)
        return None


def update(id: int, data: borrow.BorrowUpdate, db: Session):
    try:
        borrow = get_borrow(id, db)
        if not borrow:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(borrow, key, value)
            
        db.commit()
        db.refresh(borrow)

    except Exception as error:
        db.rollback()
        print(error)
        return None

    return borrow


def remove(id: int, db: Session):
    try:
        borrow = db.query(Borrow).filter(Borrow.id==id).first()
        if not borrow:
            return None
        else:
            db.delete(borrow)
            db.commit()
            return {'status': 'success'}

    except Exception as error:
        db.rollback()
        print(error)
        return {'status': 'failed'}