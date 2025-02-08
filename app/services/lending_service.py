from sqlalchemy.orm import Session
from app.models.lending import Lending
from app.schemas.lending import LendingCreate, LendingResponse
from datetime import date


class LendingService:
    @staticmethod
    def lend_book(db: Session, lending_data: LendingCreate) -> LendingResponse:
        active_lendings: int = (
            db.query(Lending)
            .filter(
                Lending.reader_id == lending_data.reader_id, Lending.return_date == None
            )
            .count()
        )
        if active_lendings >= 5:
            raise ValueError("Reader has reached the maximum limit of 5 books.")

        db_lending = Lending(**lending_data.model_dump())
        db.add(db_lending)
        db.commit()
        db.refresh(db_lending)
        return LendingResponse(**db_lending.__dict__)

    @staticmethod
    def return_book(db: Session, lending_id: int) -> LendingResponse | None:
        db_lending: Lending | None = (
            db.query(Lending).filter(Lending.id == lending_id).first()
        )
        if db_lending:
            db_lending.return_date = date.today()
            db.commit()
            db.refresh(db_lending)
            return LendingResponse(**db_lending.__dict__)
        return None
