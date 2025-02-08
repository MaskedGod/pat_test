from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1.books import router as books_router
from app.api.v1.authors import router as authors_router
from app.api.v1.readers import router as readers_router
from app.api.v1.lending import router as lending_router

settings = get_settings()

app = FastAPI()

app.include_router(books_router, prefix="/api/v1", tags=["Books"])
app.include_router(authors_router, prefix="/api/v1", tags=["Authors"])
app.include_router(readers_router, prefix="/api/v1", tags=["Readers"])
app.include_router(lending_router, prefix="/api/v1", tags=["Lending"])


@app.get("/")
def read_root():
    return {"message": "It's a Library API!"}
