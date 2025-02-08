from pydantic import BaseModel, EmailStr


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
        from_attributes = True


class ReaderUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
