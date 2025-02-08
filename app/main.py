from fastapi import FastAPI
from app.core.config import get_settings

settings = get_settings()

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Library API!"}
