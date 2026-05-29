from pydantic import BaseModel

from app.services.overpass import DEFAULT_LIMIT


class SearchRequest(BaseModel):
    key: str
    value: str
    limit: int = DEFAULT_LIMIT
