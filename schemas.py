from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel

# User Schemas
class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    role: str = "job_seeker"

class UserRead(SQLModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

# Company Schemas
class CompanyCreate(SQLModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None

class CompanyRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime

# Job Schemas
class JobCreate(SQLModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[int] = None
    is_remote: bool = False
    company_id: int
    tags: List[str] = []

class JobRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[int] = None
    is_remote: bool
    company_id: Optional[int] = None
    created_by: Optional[int] = None
    created_at: datetime
    tags: List[TagRead] = []

# Tag Schemas
class TagRead(SQLModel):
    id: int
    name: str

# Authentication Schemas
class Token(SQLModel):
    access_token: str
    token_type: str


class LoginRequest(SQLModel):
    email: str
    password: str

class ProfileCreate(SQLModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None


class ProfileUpdate(SQLModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None


class ProfileRead(SQLModel):
    id: int
    user_id: int
    full_name: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    bio: Optional[str]
    skills: Optional[str]
    experience: Optional[str]
    education: Optional[str]