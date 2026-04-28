from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from schemas import CompanyCreate, CompanyRead
from crud import create_company
from auth import get_current_user
from models import User, Company

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyRead)
def add_company(company_data: CompanyCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only employers can add companies")
    return create_company(session, company_data, current_user.id)

@router.get("/{id}", response_model=CompanyRead)
def get_company(id: int, session: Session = Depends(get_session)):
    company = session.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/", response_model=list[CompanyRead])
def list_companies(session: Session = Depends(get_session)):
    return session.exec(select(Company)).all()

@router.put("/{id}", response_model=CompanyRead)
def update_company(id: int, company_data: CompanyCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only employers can update companies")
    company = session.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if company.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own companies")
    company.name = company_data.name
    company.description = company_data.description
    company.location = company_data.location
    company.website = company_data.website
    session.commit()
    session.refresh(company)
    return company

@router.delete("/{id}", response_model=CompanyRead)
def delete_company(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["recruiter", "admin"]:
        raise HTTPException(status_code=403, detail="Only employers can delete companies")
    company = session.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if company.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own companies")
    session.delete(company)
    session.commit()
    return company
