from pydantic import BaseModel


class ReaderCreate(BaseModel):
    name: str
    email: str
    password: str


class ReaderLogin(BaseModel):
    email: str
    password: str


class ReaderResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True
