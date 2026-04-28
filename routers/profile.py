from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from auth import get_current_user
from models import User, UserProfile
from schemas import ProfileCreate, ProfileUpdate, ProfileRead
from crud import (
    create_profile,
    get_profile_by_user,
    update_profile,
    delete_profile,
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileRead)
def create_user_profile(
    data: ProfileCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "job_seeker":
        raise HTTPException(status_code=400, detail="Only job seekers can create profiles")

    existing = get_profile_by_user(session, current_user.id)

    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    return create_profile(session, current_user.id, data)

@router.get("/me", response_model=ProfileRead)
def get_my_profile(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profile = get_profile_by_user(session, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile

@router.put("/me", response_model=ProfileRead)
def update_my_profile(
    data: ProfileUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profile = get_profile_by_user(session, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return update_profile(session, profile, data)

@router.delete("/me")
def delete_my_profile(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profile = get_profile_by_user(session, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    delete_profile(session, profile)

    return {"message": "Profile deleted successfully"}