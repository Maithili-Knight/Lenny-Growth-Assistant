from fastapi import FastAPI

from app.api.routes.session import router as session_router
from app.api.routes.message import router as message_router
from app.api.routes.artifact import router as artifact_router

app = FastAPI(title="Lenny Growth Assistant")

app.include_router(session_router)
app.include_router(message_router)
app.include_router(artifact_router)


@app.get("/")
def root():
    return {"message": "Lenny Growth Assistant API is running!"}