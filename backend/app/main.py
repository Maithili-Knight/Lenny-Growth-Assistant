from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.session import router as session_router
from app.api.routes.message import router as message_router
from app.api.routes.artifact import router as artifact_router
from app.api.routes.chat import router as chat_router

app = FastAPI(title="Lenny Growth Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_router)
app.include_router(message_router)
app.include_router(artifact_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Lenny Growth Assistant API is running!"}