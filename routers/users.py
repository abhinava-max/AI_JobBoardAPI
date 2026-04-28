from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

from database import get_session
from models import User
from schemas import UserCreate, UserRead, Token, LoginRequest
from crud import create_user, get_user_by_email
from auth import create_access_token, verify_password, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserRead)
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = get_user_by_email(session, user_data.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(session, user_data)

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), session : Session = Depends(get_session)):
    user = get_user_by_email(session, form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data = {"sub": user.email, "role": user.role})
    return Token(access_token = token, token_type = "bearer")

@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

