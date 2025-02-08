from pydantic import BaseModel
from datetime import date


class AuthorCreate(BaseModel):
    name: str
    biography: str = None
    date_of_birth: date


class AuthorUpdate(BaseModel):
    name: str = None
    biography: str = None
    date_of_birth: date = None


class AuthorResponse(BaseModel):
    id: int
    name: str
    biography: str
    date_of_birth: date

    class Config:
        from_attributes = True
