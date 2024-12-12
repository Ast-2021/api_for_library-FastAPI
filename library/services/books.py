from ..models import Books
from sqlalchemy.orm import Session
from ..dto import books


def create_book(data: books.BookCreate, db):
    book = Books(title=data.title, description=data.description, 
                 author_id=data.author_id, available_quantity=data.available_quantity)
    try:
        db.add(book)
        db.commit()
        db.refresh(book)
    except Exception as error:
        db.rollback()
        print(error)
        return None
    
    return book


def get_all_books(db: Session):
    try:
        books = db.query(Books).all()
        return books
    except Exception as error:
        print(error)
        return None


def get_book(id: int, db):
    try:
        return db.query(Books).filter(Books.id==id).first()
    except Exception as error:
        print(error)
        return None


def update(id: int, data: books.BookUpdate, db: Session):
    try:
        book = db.query(Books).filter(Books.id==id).first()
        if not book:
            return None
        book.title = data.title
        book.description = data.description
        book.author_id = data.author_id
        db.add(book)
        db.commit()
        db.refresh(book)
    except Exception as error:
        db.rollback()
        print(error)
        return None

    return book


def remove(id: int, db: Session):
    try:
        book = db.query(Books).filter(Books.id==id).first()
        if not book:
            return None
        else:
            db.delete(book)
            db.commit()
            return {'status': 'success'}

    except Exception as error:
        db.rollback()
        print(error)
        return {'status': 'failed'}