from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from app.core.security import decode_access_token
from app.schemas.reader import ReaderResponse
from app.services.reader_service import ReaderService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload["sub"]


def get_current_admin(current_user: str = Depends(get_current_user)):
    db = next(get_db())
    reader: ReaderResponse | None = ReaderService.get_reader_by_email(db, current_user)
    if reader.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
