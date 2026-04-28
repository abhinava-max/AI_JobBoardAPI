# Job Board API

A FastAPI backend for a job board with user authentication, recruiter/job-seeker roles, company and job management, candidate profiles, and AI-powered job search/recommendation features.

## System Architecture

```text
Client / API Consumer
        |
        v
FastAPI application (main.py)
        |
        +-- Routers
        |   +-- /users      Authentication and current user
        |   +-- /jobs       Job CRUD, filtering, search
        |   +-- /companies  Company CRUD
        |   +-- /profiles   Job seeker profiles
        |   +-- /ai         AI search, recommendations, agent tools
        |
        +-- Auth layer (auth.py)
        |   +-- Argon2 password hashing
        |   +-- JWT access tokens
        |
        +-- Database layer
        |   +-- SQLModel models (models.py)
        |   +-- PostgreSQL connection (database.py)
        |
        +-- AI layer
            +-- LangChain / LangGraph-style agent tooling
            +-- Groq chat models for AI responses
            +-- Hugging Face embeddings
            +-- Chroma vector store for semantic search
```

The relational database stores users, companies, jobs, tags, and profiles. Chroma stores embedded job/company/profile text for semantic search and AI recommendation workflows.

## Tools Used

- FastAPI for the web API
- Uvicorn for the local development server
- SQLModel and SQLAlchemy for database models and queries
- PostgreSQL as the relational database
- Python Jose for JWT authentication
- Passlib with Argon2 for password hashing
- LangChain, LangChain Groq, and LangChain Chroma for AI workflows
- Groq for LLM inference
- Hugging Face sentence-transformer embeddings
- ChromaDB for local vector search
- python-dotenv for environment variables

## Environment Setup

Create a local environment file from the example:

```bash
cp .env.example .env
```

Then update `.env` with your local PostgreSQL credentials and API keys.

## PostgreSQL Setup

Install and start PostgreSQL, then create the database used by the app:

```bash
createdb job_board
```

If your local PostgreSQL user/password/database are different, update `DATABASE_URL` in `.env`.

Example:

```env
DATABASE_URL=postgresql://postgres:root@localhost:5432/job_board
```

The app creates tables automatically on startup through `create_db_and_tables()`.

## How to Run Locally

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your database URL, JWT secret, Groq API key, model names, and embedding settings.

4. Start PostgreSQL and make sure the `job_board` database exists:

```bash
createdb job_board
```

5. Run the API:

```bash
uvicorn main:app --reload
```

6. Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Seed Dummy Data

After configuring PostgreSQL, populate the relational database with sample users, profiles, companies, jobs, and tags:

```bash
python3 seed_dummy_data.py
```

The seed script is idempotent for users, profiles, companies, jobs, and tags, so it can be run more than once without creating duplicate records for the same emails, company names, and company/job pairs.

It also writes sample login credentials to `dummy.txt`.

Important: `seed_dummy_data.py` populates PostgreSQL only. To populate the Chroma vector database for semantic AI search, run the API and call:

```text
POST /ai/sync-vector-db
```

You can trigger it from the Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

## Useful Endpoints

- `GET /` health-style welcome route
- `POST /users/register` register a user
- `POST /users/login` get a JWT token
- `GET /users/me` get the current authenticated user
- `GET /jobs/` list and filter jobs
- `POST /jobs/` create a job as a recruiter/admin
- `GET /companies/` list companies
- `POST /companies/` create a company as a recruiter/admin
- `GET /profiles/me` get the current job seeker's profile
- `GET /ai/search` semantic vector search
- `POST /ai/recommend` recommend jobs from resume text
- `POST /ai/sync-vector-db` sync SQL jobs and companies into Chroma
- `POST /ai/ask-agent` ask the LangChain tool-using agent

## Notes

- Use `python3`, not `python`, if your shell does not map `python` to Python 3.
- Keep `.env` private. Commit `.env.example` instead.
- The local Chroma database is written to the path configured by `CHROMA_DB_PATH`.
