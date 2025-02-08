from typing import List
from sqlalchemy.orm import Session
from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderResponse
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ReaderService:
    @staticmethod
    def create_reader(db: Session, reader_data: ReaderCreate) -> ReaderResponse:
        hashed_password: str = pwd_context.hash(reader_data.password)
        db_reader = Reader(
            name=reader_data.name,
            email=reader_data.email,
            hashed_password=hashed_password,
            is_active=True,
        )
        db.add(db_reader)
        db.commit()
        db.refresh(db_reader)
        return ReaderResponse(**db_reader.__dict__)

    @staticmethod
    def get_readers(
        db: Session, skip: int = 0, limit: int = 10
    ) -> list[ReaderResponse]:
        readers: List[Reader] = db.query(Reader).offset(skip).limit(limit).all()
        return [ReaderResponse(**reader.__dict) for reader in readers]

    @staticmethod
    def get_reader_by_email(db: Session, email: str) -> ReaderResponse | None:
        db_reader: Reader | None = (
            db.query(Reader).filter(Reader.email == email).first()
        )
        if db_reader:
            return ReaderResponse(**db_reader.__dict__)
        return None

    @staticmethod
    def authenticate_reader(
        db: Session, email: str, password: str
    ) -> ReaderResponse | None:
        db_reader: ReaderResponse | None = ReaderService.get_reader_by_email(db, email)
        if db_reader and pwd_context.verify(password, db_reader.hashed_password):
            return ReaderResponse(**db_reader.__dict__)
        return None
