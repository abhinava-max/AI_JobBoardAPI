from typing import List, Optional
from sqlmodel import Session, select

from models import User, Company, Job, Tag, UserProfile
from schemas import UserCreate, CompanyCreate, JobCreate, ProfileCreate, ProfileUpdate
from auth import hash_password
from vector_store import add_company_to_vector_db, add_job_to_vector_db, add_profile_to_vector_db


# ---------------- USER CRUD ----------------

def create_user(session: Session, user_data: UserCreate) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=user_data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


# ---------------- COMPANY CRUD ----------------

def create_company(
    session: Session,
    company_data: CompanyCreate,
    user_id: int
) -> Company:
    company = Company(
        name=company_data.name,
        description=company_data.description,
        location=company_data.location,
        website=company_data.website,
        created_by=user_id
    )

    session.add(company)
    session.commit()
    session.refresh(company)
    add_company_to_vector_db(company)

    return company


# ---------------- TAG HELPER ----------------

def get_or_create_tag(session: Session, tag_name: str) -> Tag:
    tag_name = tag_name.strip().lower()

    statement = select(Tag).where(Tag.name == tag_name)
    tag = session.exec(statement).first()

    if tag:
        return tag

    tag = Tag(name=tag_name)
    session.add(tag)
    session.commit()
    session.refresh(tag)

    return tag


# ---------------- JOB CRUD ----------------

def create_job(
    session: Session,
    job_data: JobCreate,
    user_id: int
) -> Job:
    job = Job(
        title=job_data.title,
        description=job_data.description,
        location=job_data.location,
        salary=job_data.salary,
        is_remote=job_data.is_remote,
        company_id=job_data.company_id,
        created_by=user_id
    )

    for tag_name in job_data.tags:
        tag = get_or_create_tag(session, tag_name)
        job.tags.append(tag)

    session.add(job)
    session.commit()
    session.refresh(job)
    add_job_to_vector_db(job)

    return job


def get_jobs(session: Session) -> List[Job]:
    statement = select(Job)
    return list(session.exec(statement).all())

# ---------------- USER PROFILE CRUD ----------------

def create_profile(session: Session, user_id: int, data: ProfileCreate) -> UserProfile:
    profile = UserProfile(
        user_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        location=data.location,
        bio=data.bio,
        skills=data.skills,
        experience=data.experience,
        education=data.education,
    )

    session.add(profile)
    session.commit()
    session.refresh(profile)

    add_profile_to_vector_db(profile)

    return profile


def get_profile_by_user(session: Session, user_id: int) -> Optional[UserProfile]:
    statement = select(UserProfile).where(UserProfile.user_id == user_id)
    return session.exec(statement).first()


def update_profile(session: Session, profile: UserProfile, data: ProfileUpdate) -> UserProfile:
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    session.add(profile)
    session.commit()
    session.refresh(profile)

    return profile


def delete_profile(session: Session, profile: UserProfile):
    session.delete(profile)
    session.commit()