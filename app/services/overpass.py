import hashlib
import json
from linecache import cache
from platform import node
import urllib.parse
import urllib.request

DEFAULT_URL = "https://overpass.theridiid.net/api/interpreter"
DEFAULT_LIMIT = 50


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

    def search(self, tags: list[tuple[str, str]], limit: int = DEFAULT_LIMIT, enable_cache: bool = True, coords: dict | None = None, around: int = 10000) -> dict:
        cache_key = hashlib.sha256(f"{tags}:{limit}:{coords}:{around}".encode()).hexdigest()

        if enable_cache and cache_key in cache:
            return cache[cache_key]
        
        query = self.build_query(tags, limit, coords, around)
        
        raw = self._fetch(query)
        result = json.loads(raw)
        if enable_cache:
            cache[cache_key] = result
        
        return result

    def _fetch(self, query: str) -> str:
        body = urllib.parse.urlencode({"data": query}).encode("utf-8")
        request = urllib.request.Request(self.url, data=body, method="POST")
        request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
        request.add_header("Accept", "application/json")

        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8", errors="replace")
