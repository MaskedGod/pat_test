from typing import List
from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse


class AuthorService:
    @staticmethod
    def create_author(db: Session, author_data: AuthorCreate) -> AuthorResponse:
        db_author = Author(**author_data.model_dump())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return AuthorResponse(**db_author.__dict__)

    @staticmethod
    def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        name: str | None = None,
    ) -> list[AuthorResponse]:
        query = db.query(Author)

        if name:
            query = query.filter(Author.name.ilike(f"%{name}%"))

        authors: List[Author] = query.offset(skip).limit(limit).all()
        return [AuthorResponse(**author.__dict__) for author in authors]

    @staticmethod
    def get_author_by_id(db: Session, author_id: int) -> AuthorResponse | None:
        db_author: Author | None = (
            db.query(Author).filter(Author.id == author_id).first()
        )
        if db_author:
            return AuthorResponse(**db_author.__dict__)
        return None

    @staticmethod
    def update_author(
        db: Session, author_id: int, author_data: AuthorUpdate
    ) -> AuthorResponse | None:
        db_author: Author | None = (
            db.query(Author).filter(Author.id == author_id).first()
        )
        if db_author:
            for key, value in author_data.model_dump(exclude_unset=True).items():
                setattr(db_author, key, value)
            db.commit()
            db.refresh(db_author)
            return AuthorResponse(**db_author.__dict__)
        return None

    @staticmethod
    def delete_author(db: Session, author_id: int) -> AuthorResponse | None:
        db_author: Author | None = (
            db.query(Author).filter(Author.id == author_id).first()
        )
        if db_author:
            db.delete(db_author)
            db.commit()
            return AuthorResponse(**db_author.__dict__)
        return None
