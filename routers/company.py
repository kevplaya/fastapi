from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_async_db
from repositories.company_repository import CompanyRepository
from services.company_service import CompanyService

CompanyRouter = APIRouter()


def get_company_service(session: AsyncSession = Depends(get_async_db)):
    repository = CompanyRepository(session)
    return CompanyService(repository)


@CompanyRouter.get("/search")
async def autocomplete_company_name(
    query: str = Query(...),
    x_wanted_language: str = Header(...),
    service: CompanyService = Depends(get_company_service),
):
    return await service.get_autocomplete_company_names(query, x_wanted_language)


@CompanyRouter.get("/companies/{query}")
async def search_company(
    query: str, x_wanted_language: str = Header(...), service: CompanyService = Depends(get_company_service)
):
    results = await service.search_companies_by_name(query, x_wanted_language)
    return results
