from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..database import get_db
from ..models import User
from ..schemas import LoginRequest

router = APIRouter(prefix="/api/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(401, "Invalid email or password")

    # Demo project authentication. Production systems should use proper JWT/OIDC.
    # Seed credentials are documented in README.
    if payload.password not in ("admin123", "tech123"):
        raise HTTPException(401, "Invalid email or password")

    return {
        "access_token": f"demo-token-{user.id}",
        "role": user.role,
        "name": user.name
    }
