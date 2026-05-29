import urllib.error

from fastapi import APIRouter, HTTPException

from app.models.search import SearchRequest
from app.services.overpass import OverpassService

router = APIRouter()
overpass = OverpassService()


@router.post("/search")
def search(payload: SearchRequest) -> dict:
    try:
        return overpass.search(payload.key, payload.value, payload.limit)
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        detail = body.strip() or f"Overpass HTTP error: {err.code} {err.reason}"
        raise HTTPException(status_code=502, detail=detail) from err
    except urllib.error.URLError as err:
        raise HTTPException(status_code=502, detail=f"Overpass connection error: {err.reason}") from err
