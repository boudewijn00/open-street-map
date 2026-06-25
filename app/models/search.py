from typing import Any, Literal
from pydantic import BaseModel
from app.constants import DEFAULT_LIMIT

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

class Point(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]


class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Point
    properties: dict[str, Any]
    id: int | str


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Feature]
