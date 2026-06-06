import json
import urllib.error
import urllib.parse
import urllib.request

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


class GeocodeService:
    """Service to retrieve coordinates (latitude, longitude) for a location name."""

    def __init__(self, url: str = NOMINATIM_URL):
        self.url = url

    def geocode(self, location: str) -> dict | None:
        """
        Geocode a location string to coordinates.
        
        Args:
            location: Location name (e.g., "Paris, France" or "Amsterdam")
            
        Returns:
            Dictionary with 'lat' and 'lon' keys, or None if not found
        """
        results = self._fetch(location)
        if results:
            first_result = results[0]
            return {
                "lat": float(first_result["lat"]),
                "lon": float(first_result["lon"]),
            }
        return None

    def _fetch(self, location: str) -> list:
        """Fetch geocoding results from Nominatim."""
        params = {
            "q": location,
            "format": "json",
            "limit": 1,
        }
        query_string = urllib.parse.urlencode(params)
        url = f"{self.url}?{query_string}"
        
        request = urllib.request.Request(url, method="GET")
        request.add_header("User-Agent", "OSMApp/1.0")
        request.add_header("Accept", "application/json")

        with urllib.request.urlopen(request, timeout=10) as response:
            data = response.read().decode("utf-8", errors="replace")
            return json.loads(data)
