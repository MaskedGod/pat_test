from pydantic import BaseModel
from datetime import date
from typing import List


class BookCreate(BaseModel):
    title: str
    description: str
    publication_date: date
    available_copies: int
    author_ids: List[int]


class BookUpdate(BaseModel):
    title: str = None
    description: str = None
    publication_date: date = None
    available_copies: int = None
    author_ids: List[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    description: str
    publication_date: date
    available_copies: int
    authors: List[dict]

    class Config:
        from_attributes = True
