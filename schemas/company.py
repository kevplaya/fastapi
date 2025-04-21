from typing import Dict, List

from pydantic import BaseModel


class CompanyAutocompleteResponse(BaseModel):
    company_name: str


class CompanySearchResponse(BaseModel):
    company_name: List[str]


class CompanyWithTagsResponse(BaseModel):
    company_name: str
    tags: List[str]


class TagNameMultilang(BaseModel):
    tag_name: Dict[str, str]


class CompanyCreateRequest(BaseModel):
    company_name: Dict[str, str]
    tags: List[TagNameMultilang]


class TagAddRequest(BaseModel):
    tag_name: Dict[str, str]
