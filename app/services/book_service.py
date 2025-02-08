from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.lending import Lending
from app.schemas.book import BookCreate, BookUpdate, BookResponse


class BookService:
    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> BookResponse:
        db_book = Book(**book_data.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return BookResponse(**db_book.__dict__)

    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 10) -> list[BookResponse]:
        books: List[Book] = db.query(Book).offset(skip).limit(limit).all()
        return [BookResponse(**book.__dict__) for book in books]

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> BookResponse | None:
        db_book: Book | None = db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            return BookResponse(**db_book.__dict__)
        return None

    @staticmethod
    def update_book(
        db: Session, book_id: int, book_data: BookUpdate
    ) -> BookResponse | None:
        db_book: Book | None = db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            for key, value in book_data.model_dump(exclude_unset=True).items():
                setattr(db_book, key, value)
            db.commit()
            db.refresh(db_book)
            return BookResponse(**db_book.__dict__)
        return None

    @staticmethod
    def delete_book(db: Session, book_id: int, current_user: str) -> Book:
        if current_user != "admin@example.com":
            raise HTTPException(status_code=403, detail="Only admins can delete books")

        active_lendings: int = (
            db.query(Lending)
            .filter(Lending.book_id == book_id, Lending.return_date == None)
            .count()
        )
        if active_lendings > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete a book that is currently lent out",
            )

        db_book: Book | None = db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            db.delete(db_book)
            db.commit()
            return db_book
        raise HTTPException(status_code=404, detail="Book not found")
