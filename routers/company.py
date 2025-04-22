from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from config.database import get_db
from models.company import CompanySearchResponse
from repositories.company_repository import CompanyRepository
from services.company_service import CompanyService

CompanyRouter = APIRouter()


def get_company_service(session: Session = Depends(get_db)):
    repository = CompanyRepository(session)
    return CompanyService(repository)


@CompanyRouter.get("/search")
def autocomplete_company_name(
    query: str = Query(...),
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    return service.get_autocomplete_company_names(query, x_wanted_language)


@CompanyRouter.get("/companies/{query}")
def search_company(
    query: str,
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    results = service.search_companies_by_name(query, x_wanted_language)
    if not results:
        raise HTTPException(status_code=404, detail="No matching company found")
    return results


@CompanyRouter.get("/tags", response_model=list[CompanySearchResponse])
def search_by_tag(
    query: str = Query(...),
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    return service.get_companies_by_tag_name(query, x_wanted_language)
