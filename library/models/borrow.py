from sqlalchemy import Column, String, Integer, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from ..database import Base
from .books import Books

class Borrow(Base):
    __tablename__ = 'Borrow'
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('Books.id', ondelete='SET NULL'), nullable=True)
    reader_name = Column(String, nullable=False)
    date_of_issue = Column(Date, default=func.now(), nullable=False)
    return_date = Column(Date, nullable=True)

    book = relationship("Books", back_populates="borrows")