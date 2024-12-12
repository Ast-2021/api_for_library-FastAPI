from ..models import Authors
from sqlalchemy.orm import Session
from ..dto import authors


def create_author(data: authors.AuthorCreate, db):
    author = Authors(name=data.name, last_name=data.last_name, date_of_birth=data.date_of_birth)

    try:
        db.add(author)
        db.commit()
        db.refresh(author)
    except Exception as error:
        db.rollback()
        print(error)
        return None
    
    return author


def get_all_authors(db: Session):
    try:
        authors = db.query(Authors).all()
        return authors
    except Exception as error:
        print(error)
        return None


def get_author(id: int, db):
    try:
        return db.query(Authors).filter(Authors.id==id).first()
    except Exception as error:
        print(error)
        return None


def update(id: int, data: authors.AuthorUpdate, db: Session):
    try:
        author = db.query(Authors).filter(Authors.id==id).first()
        if not author:
            return None
        author.name = data.name
        author.last_name = data.last_name
        author.date_of_birth = data.date_of_birth
        db.add(author)
        db.commit()
        db.refresh(author)
    except Exception as error:
        db.rollback()
        print(error)
        return None

    return author


def remove(id: int, db: Session):
    try:
        author = db.query(Authors).filter(Authors.id==id).first()
        if not author:
            return None
        else:
            db.delete(author)
            db.commit()
            return {'status': 'success'}

    except Exception as error:
        db.rollback()
        print(error)
        return {'status': 'failed'}