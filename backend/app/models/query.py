from pydantic import BaseModel
from typing import Optional, List

class Query(BaseModel):
    text: str
    doc_type: Optional[str] = None
    date_range: Optional[List[str]] = None
    citation_min: Optional[int] = None
    field_of_research: Optional[str] = None
