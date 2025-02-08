from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.reader import ReaderCreate, ReaderLogin, ReaderResponse, ReaderUpdate
from app.services.reader_service import ReaderService
from app.utils.auth import get_current_admin, get_current_user

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
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin),
) -> list[ReaderResponse]:
    return ReaderService.get_readers(db, skip, limit)


@router.put("/{reader_id}/role", response_model=ReaderResponse)
def update_reader_role(
    reader_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_admin),
):
    db_reader = ReaderService.get_reader_by_id(db, reader_id)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    db_reader.role = role
    db.commit()
    db.refresh(db_reader)
    return db_reader


@router.put("/me", response_model=ReaderResponse)
def update_reader_info(
    reader_data: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> ReaderResponse:
    db_reader: ReaderResponse | None = ReaderService.get_reader_by_email(
        db, current_user
    )
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    updated_reader: ReaderResponse | None = ReaderService.update_reader(
        db, db_reader.id, reader_data
    )
    if not updated_reader:
        raise HTTPException(status_code=500, detail="Failed to update reader info")
    return updated_reader
