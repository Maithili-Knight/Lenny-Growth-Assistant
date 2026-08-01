from fastapi import FastAPI

from app.api.session import router as session_router
from app.api.message import router as message_router

app = FastAPI(title="Lenny Growth Assistant")

app.include_router(session_router)
app.include_router(message_router)


@app.get("/")
def root():
    return {"message": "Lenny Growth Assistant API is running!"}