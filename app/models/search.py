from pydantic import BaseModel

from app.services.overpass import DEFAULT_LIMIT


class SearchRequest(BaseModel):
    key: str
    value: str
    location: str | None = None
    limit: int = DEFAULT_LIMIT


class GeocodeRequest(BaseModel):
    location: str


class GeocodeResponse(BaseModel):
    lat: float
    lon: float
    display_name: str
