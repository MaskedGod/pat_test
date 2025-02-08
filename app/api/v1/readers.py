from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.reader import ReaderCreate, ReaderLogin, ReaderResponse
from app.services.reader_service import ReaderService

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.post("/register", response_model=ReaderResponse)
def register_reader(
    reader_data: ReaderCreate, db: Session = Depends(get_db)
) -> ReaderResponse:
    return ReaderService.create_reader(db, reader_data)


@router.post("/login")
def login_reader(
    reader_data: ReaderLogin, db: Session = Depends(get_db)
) -> dict[str, str]:
    reader: ReaderResponse | None = ReaderService.authenticate_reader(
        db, reader_data.email, reader_data.password
    )
    if not reader:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}


@router.get("/", response_model=list[ReaderResponse])
def get_readers(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[ReaderResponse]:
    return ReaderService.get_readers(db, skip, limit)
