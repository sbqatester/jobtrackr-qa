import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, text

# Default matches docker-compose.yml (host port 5433).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://jobtrackr:jobtrackr_pw@localhost:5433/jobtrackr",
)
# Change this in real use; set it as an environment variable.
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
TOKEN_MINUTES = 60

engine = create_engine(DATABASE_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)


app = FastAPI(title="JobTrackr QA API", version="0.1.0")


# ---------- Models ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class UserLogin(BaseModel):
    email: str
    password: str


class ApplicationIn(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=150)
    status: Literal["Applied", "Screening", "Interview", "Offer", "Rejected"] = "Applied"
    salary: int = Field(gt=0)


# ---------- Auth helpers ----------
def create_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expires}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_id(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> int:
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")



# ---------- Health ----------
@app.get("/health")
def health():
    """Check that the API can reach the database."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}")
    return {"status": "ok", "database": "connected"}


# ---------- Auth endpoints ----------
@app.post("/auth/register", status_code=201)
def register(data: UserCreate):
    with engine.begin() as conn:
        exists = conn.execute(
            text("SELECT id FROM users WHERE email = :email"), {"email": data.email}
        ).first()
        if exists:
            raise HTTPException(status_code=409, detail="Email already registered")
        row = conn.execute(
            text(
                "INSERT INTO users (email, password_hash) "
                "VALUES (:email, :hash) RETURNING id, email"
            ),
            {"email": data.email, "hash": pwd_context.hash(data.password)},
        ).first()
    return {"id": row.id, "email": row.email}


@app.post("/auth/login")
def login(data: UserLogin):
    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT id, password_hash FROM users WHERE email = :email"),
            {"email": data.email},
        ).first()
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": create_token(user.id), "token_type": "bearer"}


# ---------- Application endpoints ----------
@app.get("/applications")
def list_applications(user_id: int = Depends(get_current_user_id)):
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT id, company, role, status, salary FROM applications "
                "WHERE user_id = :uid ORDER BY id"
            ),
            {"uid": user_id},
        ).mappings().all()
    return [dict(r) for r in rows]


@app.post("/applications", status_code=201)
def create_application(data: ApplicationIn, user_id: int = Depends(get_current_user_id)):
    with engine.begin() as conn:
        row = conn.execute(
            text(
                "INSERT INTO applications (user_id, company, role, status, salary) "
                "VALUES (:uid, :company, :role, :status, :salary) "
                "RETURNING id, company, role, status, salary"
            ),
            {"uid": user_id, **data.model_dump()},
        ).mappings().first()
    return dict(row)


@app.put("/applications/{app_id}")
def update_application(
    app_id: int, data: ApplicationIn, user_id: int = Depends(get_current_user_id)
):
    with engine.begin() as conn:
        row = conn.execute(
            text(
                "UPDATE applications SET company=:company, role=:role, "
                "status=:status, salary=:salary "
                "WHERE id=:id AND user_id=:uid "
                "RETURNING id, company, role, status, salary"
            ),
            {"id": app_id, "uid": user_id, **data.model_dump()},
        ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")
    return dict(row)


@app.delete("/applications/{app_id}")
def delete_application(app_id: int, user_id: int = Depends(get_current_user_id)):
    with engine.begin() as conn:
        row = conn.execute(
            text("DELETE FROM applications WHERE id=:id AND user_id=:uid RETURNING id"),
            {"id": app_id, "uid": user_id},
        ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"deleted": app_id}


# Mount the UI last so it doesn't shadow the API routes.
app.mount(
    "/ui",
    StaticFiles(directory=Path(__file__).resolve().parent.parent / "frontend", html=True),
    name="frontend",
)
