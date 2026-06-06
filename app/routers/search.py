import urllib.error

from fastapi import APIRouter, HTTPException

from app.models.search import SearchRequest, GeocodeRequest, GeocodeResponse
from app.services.overpass import OverpassService
from app.services.geocode import GeocodeService

router = APIRouter()
overpass = OverpassService()
geocode = GeocodeService()


@router.post("/search")
def search(payload: SearchRequest) -> dict:
    try:
        coords = None
        if payload.location:
            coords = geocode.geocode(payload.location)
        
        return overpass.search(payload.key, payload.value, payload.limit, coords)
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        detail = body.strip() or f"Overpass HTTP error: {err.code} {err.reason}"
        raise HTTPException(status_code=502, detail=detail) from err
    except urllib.error.URLError as err:
        raise HTTPException(status_code=502, detail=f"Overpass connection error: {err.reason}") from err


@router.post("/geocode", response_model=GeocodeResponse)
def geocode_location(payload: GeocodeRequest) -> dict:
    try:
        result = geocode.geocode(payload.location)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Location not found: {payload.location}")
        return result
    except urllib.error.HTTPError as err:
        raise HTTPException(status_code=502, detail=f"Geocoding HTTP error: {err.code} {err.reason}") from err
    except urllib.error.URLError as err:
        raise HTTPException(status_code=502, detail=f"Geocoding connection error: {err.reason}") from err
