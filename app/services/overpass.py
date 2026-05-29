import json
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_URL = "http://127.0.0.1:12345/api/interpreter"
DEFAULT_LIMIT = 5


class OverpassService:
    def __init__(self, url: str = DEFAULT_URL):
        self.url = url

    def build_query(self, key: str, value: str, limit: int = DEFAULT_LIMIT) -> str:
        return "\n".join([
            "[out:json];",
            f'node["{key}"="{value}"];',
            f"out {limit};",
        ])

    def search(self, key: str, value: str, limit: int = DEFAULT_LIMIT) -> dict:
        query = self.build_query(key, value, limit)
        raw = self._fetch(query)
        return json.loads(raw)

    def _fetch(self, query: str) -> str:
        body = urllib.parse.urlencode({"data": query}).encode("utf-8")
        request = urllib.request.Request(self.url, data=body, method="POST")
        request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
        request.add_header("Accept", "application/json")

        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8", errors="replace")
