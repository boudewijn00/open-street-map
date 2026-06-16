from pydantic import BaseModel

from app.services.overpass import DEFAULT_LIMIT


class SearchRequest(BaseModel):
    tags: list[tuple[str, str]]
    location: str | None = None
    limit: int = DEFAULT_LIMIT
    around: int = 10000
    cache: bool = True


class GeocodeRequest(BaseModel):
    location: str


class GeocodeResponse(BaseModel):
    lat: float
    lon: float
    display_name: str
