from typing import List, Dict
from sqlmodel import select

from langchain_core.tools import tool

from database import get_session
from models import Job, Company, UserProfile
from vector_store import semantic_search


# ---------------- RAW TOOL FUNCTIONS ----------------

def get_jobs_tool(limit: int = 10) -> List[Dict]:
    with next(get_session()) as session:
        jobs = session.exec(select(Job)).all()

        return [
            {
                "job_id": job.id,
                "title": job.title,
                "description": job.description,
                "location": job.location,
                "salary": job.salary,
                "company_id": job.company_id,
                "is_remote": job.is_remote,
            }
            for job in jobs[:limit]
        ]


def get_companies_tool(limit: int = 10) -> List[Dict]:
    with next(get_session()) as session:
        companies = session.exec(select(Company)).all()

        return [
            {
                "company_id": company.id,
                "name": company.name,
                "description": company.description,
                "location": company.location,
                "website": company.website,
            }
            for company in companies[:limit]
        ]


def vector_search_tool(query: str) -> List[Dict]:
    results = semantic_search(query=query, k=5)

    return [
        {
            "content": item["content"],
            "metadata": item["metadata"],
            "score": item["score"],
        }
        for item in results
    ]


def get_profiles_tool(limit: int = 10) -> List[Dict]:
    with next(get_session()) as session:
        profiles = session.exec(select(UserProfile)).all()

        return [
            {
                "profile_id": profile.id,
                "user_id": profile.user_id,
                "full_name": profile.full_name,
                "skills": profile.skills,
                "experience": profile.experience,
                "location": profile.location,
                "bio": profile.bio,
            }
            for profile in profiles[:limit]
        ]


# ---------------- LANGCHAIN TOOL WRAPPERS ----------------

@tool
def vector_search_tool(query: str):
    """Search jobs using semantic similarity."""
    results = semantic_search(query=query, k=5)

    return [
        {
            "content": r["content"],
            "metadata": r["metadata"],
            "score": r["score"],
        }
        for r in results
    ]


@tool
def get_jobs_tool(limit: int = 10):
    """Fetch jobs from the system."""
    with next(get_session()) as session:
        jobs = session.exec(select(Job)).all()

        return [
            {
                "job_id": job.id,
                "title": job.title,
                "description": job.description,
                "location": job.location,
                "salary": job.salary,
            }
            for job in jobs[:limit]
        ]


@tool
def get_profiles_tool(limit: int = 10):
    """Fetch candidate profiles."""
    with next(get_session()) as session:
        profiles = session.exec(select(UserProfile)).all()

        return [
            {
                "profile_id": p.id,
                "skills": p.skills,
                "experience": p.experience,
                "location": p.location,
            }
            for p in profiles[:limit]
        ]


@tool
def get_companies_tool(limit: int = 10):
    """Fetch companies."""
    with next(get_session()) as session:
        companies = session.exec(select(Company)).all()

        return [
            {
                "company_id": c.id,
                "name": c.name,
                "location": c.location,
            }
            for c in companies[:limit]
        ]


# ---------------- FINAL TOOL LIST ----------------

tools = [
    get_jobs_tool,
    vector_search_tool,
    get_profiles_tool,
    get_companies_tool,
]