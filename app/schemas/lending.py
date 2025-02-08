from pydantic import BaseModel
from datetime import date


class LendingCreate(BaseModel):
    book_id: int
    reader_id: int
    issue_date: date
    return_date: date = None


class LendingResponse(BaseModel):
    id: int
    book_id: int
    reader_id: int
    issue_date: date
    return_date: date

    class Config:
        from_attributes = True
