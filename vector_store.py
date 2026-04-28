import os
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from models import Job, Company

load_dotenv()

HUGGINGFACE_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL")
HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")

embeddings = HuggingFaceEmbeddings(
    model_name = HUGGINGFACE_EMBEDDING_MODEL,
    encode_kwargs = {'normalize_embeddings': True}
)

vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)

def format_job_for_db(job: Job) -> Document:
    page_content = f"""
    Role: {job.title}
    Company: {job.company.name if job.company else "Unknown Company"}
    Location: {job.location}
    Description: {job.description}
    """

    metadata = {
        "job_id": job.id,
        "company_id": job.company_id,
        "title": job.title,
        "location": job.location,
        "company_name": job.company.name if job.company else "Unknown Company",
    }

    return Document(page_content=page_content, metadata=metadata)

def format_company_for_db(company: Company) -> Document:
    page_content = f"""
    Company: {company.name}
    Description: {company.description}
    Location: {company.location}
    Website: {company.website}
    """

    metadata = {
        "company_id": company.id,
        "name": company.name,
        "location": company.location,
    }

    return Document(page_content=page_content, metadata=metadata)

def format_profile_for_db(profile):
    return Document(
        page_content=f"""
        Name: {profile.full_name}
        Location: {profile.location}
        Skills: {profile.skills}
        Experience: {profile.experience}
        Education: {profile.education}
        Bio: {profile.bio}
        """,
        metadata={
            "type": "profile",
            "profile_id": profile.id,
            "user_id": profile.user_id
        }
    )

def add_company_to_vector_db(company: Company):
    doc = format_company_for_db(company)
    vector_db.add_documents([doc], ids=[f"comp_{company.id}"])

def add_job_to_vector_db(job: Job):
    doc = format_job_for_db(job)
    vector_db.add_documents([doc], ids=[f"job_{job.id}"])

def add_profile_to_vector_db(profile):
    vector_db.add_documents(
        [format_profile_for_db(profile)],
        ids=[f"profile_{profile.id}"]
    )

def semantic_search(query: str, k: int = 5) -> list[Document]:
    results = vector_db.similarity_search_with_score(query, k=k)
    output = []
    for doc, score in results:
        output.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": score,
        })
    return output