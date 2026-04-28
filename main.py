from fastapi import FastAPI, Depends
from database import create_db_and_tables
from routers import users, jobs, companies, ai_agents, profile

app = FastAPI(title="Job Board API", description="API for Job Board", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Welcome to Job Board API"}

app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(companies.router)
app.include_router(ai_agents.router)
app.include_router(profile.router)

