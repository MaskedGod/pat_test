from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.lending import LendingCreate, LendingResponse
from app.services.lending_service import LendingService

router = APIRouter(prefix="/lending", tags=["Lending"])


@router.post("/", response_model=LendingResponse)
def lend_book(
    lending_data: LendingCreate, db: Session = Depends(get_db)
) -> LendingResponse:
    try:
        return LendingService.lend_book(db, lending_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{lending_id}", response_model=LendingResponse)
def return_book(lending_id: int, db: Session = Depends(get_db)) -> LendingResponse:
    lending: LendingResponse | None = LendingService.return_book(db, lending_id)
    if not lending:
        raise HTTPException(status_code=404, detail="Lending not found")
    return lending
