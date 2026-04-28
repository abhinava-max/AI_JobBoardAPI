from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class JobTagLink(SQLModel, table=True):
    job_id: Optional[int] = Field(default=None, foreign_key="job.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    password: str = Field(nullable=False)
    role: str = Field(default="job_seeker", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    jobs: List["Job"] = Relationship(back_populates="creator")
    companies: List["Company"] = Relationship(back_populates="creator")
    profile: Optional["UserProfile"] = Relationship(back_populates="user")


class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    creator: Optional[User] = Relationship(back_populates="companies")
    jobs: List["Job"] = Relationship(back_populates="company")


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[int] = None
    is_remote: bool = False

    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    creator: Optional[User] = Relationship(back_populates="jobs")
    company: Optional[Company] = Relationship(back_populates="jobs")
    tags: List["Tag"] = Relationship(back_populates="jobs", link_model=JobTagLink)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    jobs: List[Job] = Relationship(back_populates="tags", link_model=JobTagLink)

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", unique=True)

    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None

    resume_text: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="profile")