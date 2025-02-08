from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    publication_date = Column(Date)
    available_copies = Column(Integer, default=0)

    authors = relationship("Author", secondary="book_authors", back_populates="books")
