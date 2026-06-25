import hashlib
import json
import urllib.parse
import urllib.request

from linecache import cache
from app.constants import DEFAULT_LIMIT
from app.models.search import Point, Feature, FeatureCollection

DEFAULT_URL = "https://overpass.theridiid.net/api/interpreter"


class OverpassService:
    def __init__(self, url: str = DEFAULT_URL):
        self.url = url

    def build_query(self, tags: list[tuple[str, str]], limit: int = DEFAULT_LIMIT, coords: dict | None = None, around: int = 10000) -> str:
        filters = "".join(
                f'["{key}"="{value}"]'
                for key, value in tags
            )
        
        if coords:
            lat = coords["lat"]
            lon = coords["lon"]
            
            return (
                f"[out:json];\n"
                f"nwr{filters}"
                f"(around:{around},{lat},{lon});\n"
                f"out;"
            )
        
        return (
            f"[out:json];\n"
            f"nwr{filters};\n"
            f"out;"
        )

    def search(self, tags: list[tuple[str, str]], limit: int = DEFAULT_LIMIT, enable_cache: bool = True, coords: dict | None = None, around: int = 10000) -> FeatureCollection:
        cache_key = hashlib.sha256(f"{tags}:{limit}:{coords}:{around}".encode()).hexdigest()

        if enable_cache and cache_key in cache:
            result = cache[cache_key]
        else:
            query = self.build_query(tags, limit, coords, around)
            print(f"DEBUG: Query being sent to Overpass API:\n{query}")
            raw = self._fetch(query)
            print(f"DEBUG: Raw response from Overpass API: {raw[:500]}")
            
            if raw.startswith("<?xml") or "<Error>" in raw or "error" in raw.lower():
                print("DEBUG: Error response detected")
                return FeatureCollection(
                    type="FeatureCollection",
                    features=[]
                )
            
            result = json.loads(raw)
            print(f"DEBUG: Parsed JSON result: {result}")

            if enable_cache:
                cache[cache_key] = result
        
        feature_collection = FeatureCollection(
            type="FeatureCollection",
            features=[
                Feature(
                    type="Feature",
                    geometry=Point(type="Point", coordinates=(element["lon"], element["lat"])),
                    properties=element.get("tags", {}),
                    id=element['id']
                )
                for element in result.get("elements", [])
                if element["type"] == "node"
            ]
        )

        return feature_collection
    def _fetch(self, query: str) -> str:
        body = urllib.parse.urlencode({"data": query}).encode("utf-8")
        request = urllib.request.Request(self.url, data=body, method="POST")
        request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
        request.add_header("Accept", "application/json")

        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8", errors="replace")
