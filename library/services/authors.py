from ..models import Authors
from ..dto import authors
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def create_author(data: authors.AuthorCreate, db: Session):
    try:
        author = Authors(name=data.name, last_name=data.last_name, 
                         date_of_birth=data.date_of_birth)
        db.add(author)
        db.commit()
        db.refresh(author)
        return author

    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


def get_all_authors(db: Session):
    authors = db.query(Authors).all()
    return authors


def get_author(id: int, db: Session):
    author = db.query(Authors).filter(Authors.id==id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


def update(id: int, data: authors.AuthorUpdate, db: Session):
    try:
        author = db.query(Authors).filter(Authors.id==id).first()
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Author not found")
        author.name = data.name
        author.last_name = data.last_name
        author.date_of_birth = data.date_of_birth
        db.add(author)
        db.commit()
        db.refresh(author)
        return author
    
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


def remove(id: int, db: Session):
    try:
        author = db.query(Authors).filter(Authors.id==id).first()
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Author not found")
        else:
            db.delete(author)
            db.commit()
    except Exception:
        db.rollback()
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="An unexpected error occurred. Please try again later.")