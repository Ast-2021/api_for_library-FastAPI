from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .authors import Authors

class Books(Base):
    __tablename__ = 'Books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('Authors.id', ondelete='SET NULL'), nullable=True)
    available_quantity = Column(Integer, default=10)

    author = relationship('Authors', back_populates='books')
    borrows = relationship("Borrow", back_populates="book", lazy='dynamic')