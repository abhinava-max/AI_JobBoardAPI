import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from langchain_groq import ChatGroq
from prompts import prompt_ask_ai, recommend_prompt, summarize, improve_description_prompt
from database import get_session
from models import Job, Company
from vector_store import add_job_to_vector_db, add_company_to_vector_db, semantic_search
from langchain.agents import create_agent
from ai_services import tools
from typing import List

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI"])

llm_thinking = ChatGroq(
    model=os.getenv("GROQ_MODEL_THINKING"), 
    temperature=0.1
    )
llm_medium = ChatGroq(
    model=os.getenv("GROQ_MODEL_MEDIUM"), 
    temperature=0.1
    )
llm_fast = ChatGroq(
    model=os.getenv("GROQ_MODEL_FAST"),
    temperature=0.1,
)

agent = create_agent(
    model=llm_medium,
    tools=tools,
    system_prompt="""
You are an AI agent for a Job Board API.

You can use tools to:
- search jobs semantically
- fetch jobs
- fetch companies
- fetch candidate profiles

Rules:
- Always use tools when the user asks about jobs, companies, or candidates.
- Never invent jobs, companies, salaries, locations, or candidate details.
- Only use data returned by tools.
- Return concise results.
- Do not use markdown.
- Do not explain your reasoning.
- Return only valid JSON.
- The final response must be a JSON object, not a JSON string.
- Do not wrap JSON inside quotes.
- Do not add text before or after JSON.

Required final output format:

{
  "answer": "short natural language summary",
  "jobs": [
    {
      "job_id": 0,
      "title": "",
      "company": "",
      "location": "",
      "salary": null,
      "reason": ""
    }
  ],
  "companies": [],
  "candidates": [],
  "note": ""
}

If no relevant data is found, return:

{
  "answer": "No relevant data found.",
  "jobs": [],
  "companies": [],
  "candidates": [],
  "note": "No matching records were available from the tools."
}
"""
)

llm_chain_ask_ai = prompt_ask_ai | llm_medium
llm_chain_summarize = summarize | llm_fast
llm_chain_recommend = recommend_prompt | llm_thinking
llm_chain_improve = improve_description_prompt | llm_fast


@router.post("/sync-vector-db")
def sync_vector_db(session: Session = Depends(get_session)):
    jobs = session.exec(select(Job)).all()
    companies = session.exec(select(Company)).all()

    for job in jobs:
        add_job_to_vector_db(job)
    for company in companies:
        add_company_to_vector_db(company)

    return {
        "message": "Vector database synced successfully",
        "jobs_synced": len(jobs),
        "companies_synced": len(companies),
    }


@router.get("/search")
def search_ai(query: str, limit: int = 5):
    results = semantic_search(query=query, k=limit)

    return {
        "query": query,
        "results": results,
    }

@router.get("/ask-ai")
def ask_ai(query: str, limit: int = 5):
    results = semantic_search(query=query, k=limit)
    context = ""

    for item in results:
        context += f"""
        Content:
        {item["content"]}

        Metadata:
        {item["metadata"]}

        Score:
        {item["score"]}

        ---
        """

    answer = llm_chain_ask_ai.invoke({
        "context": context, 
        "question": query})
    
    return {
        "query": query,
        "answer": answer.content,
        "source": results,
    }

@router.post("/recommend")
def recommend_jobs(resume_text: str, limit: int = 5):
    resume_summary = llm_chain_summarize.invoke({
        "resume": resume_text
    })

    results = semantic_search(query=resume_summary.content, k=limit)
    context = ""

    for item in results:
        context += f"""
        Content:
        {item["content"]}

        Metadata:
        {item["metadata"]}

        Score:
        {item["score"]}

        ---
        """

    answer = llm_chain_recommend.invoke({
        "context": context, 
        "question": f"Recommend the best jobs for this candidate profile: {resume_summary.content}"})
    
    return {
        "resume_summary": resume_summary.content,
        "recommendations": answer.content,
        "source": results,
    }

@router.post("/improve-description")
def improve_description(description: str, improvement_mode: int):
    if improvement_mode == 1:
        improvement_prompt = "short"
    elif improvement_mode == 2:
        improvement_prompt = "detailed"
    elif improvement_mode == 3:
        improvement_prompt = "marketing"
    
    answer = llm_chain_improve.invoke({
        "description": description,
        "improvement_mode": improvement_prompt
    })
    
    return {
        "improved_description": answer.content,
        "improvement_mode": improvement_prompt,
    }

@router.post("/ask-agent")
def ask_agent(task: str):
    import json
    try:
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": task}
            ]
        })

        content = response["messages"][-1].content

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {
                "answer": content,
                "jobs": [],
                "companies": [],
                "candidates": [],
                "note": "Response was not valid JSON"
            }

        return {
            "task": task,
            "result": parsed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))