from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.reader import ReaderCreate, ReaderLogin, ReaderResponse
from app.services.reader_service import ReaderService
from datetime import timedelta
from app.core.config import get_settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ReaderResponse)
def register(
    reader_data: ReaderCreate, db: Session = Depends(get_db)
) -> ReaderResponse:
    reader_data.password = hash_password(reader_data.password)
    return ReaderService.create_reader(db, reader_data)


@router.post("/login")
def login(reader_data: ReaderLogin, db: Session = Depends(get_db)) -> dict[str, str]:
    reader: ReaderResponse | None = ReaderService.authenticate_reader(
        db, reader_data.email, reader_data.password
    )
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": reader.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
