import os

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

# Default matches docker-compose.yml (host port 5433).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://jobtrackr:jobtrackr_pw@localhost:5433/jobtrackr",
)

engine = create_engine(DATABASE_URL)

app = FastAPI(title="JobTrackr QA API", version="0.1.0")


@app.get("/health")
def health():
    """Check that the API can reach the database."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}")
    return {"status": "ok", "database": "connected"}
