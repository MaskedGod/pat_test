from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.services.author_service import AuthorService

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorResponse)
def create_author(
    author_data: AuthorCreate, db: Session = Depends(get_db)
) -> AuthorResponse:
    return AuthorService.create_author(db, author_data)


@router.get("/", response_model=list[AuthorResponse])
def get_authors(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[AuthorResponse]:
    return AuthorService.get_authors(db, skip, limit)


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)) -> AuthorResponse:
    author: AuthorResponse | None = AuthorService.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    author_id: int, author_data: AuthorUpdate, db: Session = Depends(get_db)
) -> AuthorResponse:
    author: AuthorResponse | None = AuthorService.update_author(
        db, author_id, author_data
    )
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.delete("/{author_id}", response_model=AuthorResponse)
def delete_author(author_id: int, db: Session = Depends(get_db)) -> AuthorResponse:
    author: AuthorResponse | None = AuthorService.delete_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author
