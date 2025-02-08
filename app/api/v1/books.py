from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin),
) -> BookResponse:
    return BookService.create_book(db, book_data)


@router.get("/", response_model=list[BookResponse])
def get_books(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[BookResponse]:
    return BookService.get_books(db, skip, limit)


@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)) -> BookResponse:
    book: BookResponse | None = BookService.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)
) -> BookResponse:
    book: BookResponse | None = BookService.update_book(db, book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", response_model=BookResponse)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin),
) -> BookResponse:
    book: BookResponse | None = BookService.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
