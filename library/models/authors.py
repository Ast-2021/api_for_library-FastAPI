from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from ..database import Base


class Authors(Base):
    __tablename__ = 'Authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    date_of_birth = Column(Date)

    books = relationship("Books", back_populates="author")