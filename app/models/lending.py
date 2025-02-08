from sqlalchemy import Column, Integer, ForeignKey, Date
from app.core.database import Base


class Lending(Base):
    __tablename__ = "lendings"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    issue_date = Column(Date)
    return_date = Column(Date)
