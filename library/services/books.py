from ..models import Books
from sqlalchemy.orm import Session
from ..dto import books
from fastapi import HTTPException, status


def create_book(data: books.BookCreate, db):
    book = Books(title=data.title, description=data.description, 
                 author_id=data.author_id, available_quantity=data.available_quantity)
    try:
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


def get_all_books(db: Session):
    books = db.query(Books).all()
    return books


def get_book(id: int, db):
    book =  db.query(Books).filter(Books.id==id).first()
    if book is not None:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'message': 'book not found'})


def update(id: int, data: books.BookUpdate, db: Session):
    book = db.query(Books).filter(Books.id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'message': 'book not found'})
    try:
        book.title = data.title
        book.description = data.description
        book.author_id = data.author_id
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'message': 'Book data could not be updated'})


def remove(id: int, db: Session):
    book = db.query(Books).filter(Books.id==id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'message': 'book not found'})
    try:
        db.delete(book)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
