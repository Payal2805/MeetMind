
from fastapi import FastAPI, HTTPException

from app.database import test_connection
from app.routers.meetings import router as meetings_router
from app.routers.audio import router as audio_router


app = FastAPI(
    title="MeetMind API",
    description="AI-powered meeting assistant",
    version="0.1.0",
)


# Register API routers
app.include_router(meetings_router)
app.include_router(audio_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to MeetMind!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/database")
def database_health_check():
    try:
        result = test_connection()
        return {
            "status": "connected",
            "database_test": result,
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed.",
        )
