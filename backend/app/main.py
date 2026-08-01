from fastapi import FastAPI

app = FastAPI(
    title="The Lenny Growth Assistant",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Lenny Growth Assistant API is running 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }