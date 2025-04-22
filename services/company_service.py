from models.company import Company
from repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    def get_autocomplete_company_names(self, keyword: str, lang: str):
        names = self.company_repository.autocomplete_company_name(keyword, lang)
        return [{"company_name": name} for name in names]

    def search_companies_by_name(self, keyword: str, lang: str):
        company = self.company_repository.search_company_by_name(keyword)
        if not company:
            return []
        return {
            "company_name": next((name.name for name in company.names if name.lang == lang), ""),
            "tags": [tag_name.name for tag in company.tags for tag_name in tag.names if tag_name.lang == lang],
        }

    def get_companies_by_tag_name(self, tag_keyword: str, lang: str) -> list[dict]:
        def resolve_company_name(company: Company, lang: str) -> str:
            for name in company.names:
                if name.lang == lang:
                    return name.name
            return company.names[0].name if company.names else ""

        companies = self.company_repository.search_companies_by_tag_name(tag_keyword, lang)
        seen_ids = set()
        result = [
            {"company_name": resolve_company_name(company, lang)} for company in companies if company.id not in seen_ids
        ]
        return result
