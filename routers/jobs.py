from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional, List

from database import get_session
from schemas import JobCreate, JobRead
from crud import create_job, get_jobs, get_or_create_tag
from models import User, Job, Tag
from auth import get_current_user
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ---------------- CREATE JOB ----------------
@router.post("/", response_model=JobRead)
def add_job(
    job_data: JobCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only employers can add jobs")

    return create_job(session, job_data, current_user.id)


# ---------------- LIST JOBS (FILTERS) ----------------
@router.get("/", response_model=list[JobRead])
def get_jobs(
    location: str | None = None,
    is_remote: bool | None = None,
    company_id: int | None = None,
    min_salary: int | None = None,
    max_salary: int | None = None,
    tags: list[str] | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    statement = select(Job).options(selectinload(Job.tags))

    # -------- FILTERS --------

    if location:
        statement = statement.where(Job.location == location)

    if is_remote is not None:
        statement = statement.where(Job.is_remote == is_remote)

    if company_id:
        statement = statement.where(Job.company_id == company_id)

    if min_salary:
        statement = statement.where(Job.salary >= min_salary)

    if max_salary:
        statement = statement.where(Job.salary <= max_salary)

    if search:
        statement = statement.where(
            Job.title.contains(search) |
            Job.description.contains(search)
        )

    if tags:
        statement = statement.join(Job.tags).where(Tag.name.in_(tags))

    # -------- PAGINATION --------
    statement = statement.offset(skip).limit(limit)

    results = session.exec(statement).all()

    return results


# ---------------- DELETE JOB ----------------
@router.delete("/{id}", response_model=JobRead)
def delete_job(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only employers can delete jobs")

    job = session.get(Job, id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own jobs")

    session.delete(job)
    session.commit()

    return job


# ---------------- UPDATE JOB ----------------
@router.put("/{id}", response_model=JobRead)
def update_job(
    id: int,
    job_data: JobCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only employers can update jobs")

    job = session.get(Job, id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own jobs")

    # update basic fields
    job.title = job_data.title
    job.description = job_data.description
    job.location = job_data.location
    job.salary = job_data.salary
    job.is_remote = job_data.is_remote
    job.company_id = job_data.company_id

    # FIX: update tags properly
    job.tags.clear()

    if job_data.tags:
        for tag_name in job_data.tags:
            tag = get_or_create_tag(session, tag_name)
            job.tags.append(tag)

    session.add(job)
    session.commit()
    session.refresh(job)

    return job