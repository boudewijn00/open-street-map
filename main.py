import json
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_URL = "http://127.0.0.1:12345/api/interpreter"
DEFAULT_LIMIT = 5


def build_query(key, value, limit=DEFAULT_LIMIT):
	return "\n".join([
"[out:json];",
f'nwr["{key}"="{value}"];',
f"out {limit};",
])


def fetch_overpass(query, url=DEFAULT_URL):
	body = urllib.parse.urlencode({"data": query}).encode("utf-8")
	request = urllib.request.Request(url, data=body, method="POST")
	request.add_header("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
	request.add_header("Accept", "application/json")

	with urllib.request.urlopen(request, timeout=60) as response:
		return response.read().decode("utf-8", errors="replace")


def element_position(element):
	if "lat" in element and "lon" in element:
		return element["lat"], element["lon"]
	center = element.get("center") or {}
	return center.get("lat"), center.get("lon")


def print_results(payload):
	data = json.loads(payload)
	elements = data.get("elements", [])
	if not elements:
		print("No matching objects found.")
		return

	for element in elements:
		tags = element.get("tags", {})
		name = tags.get("name", "<no name>")
		lat, lon = element_position(element)
		location = f"{lat}, {lon}" if lat is not None and lon is not None else "<no position>"
		print(f"{element.get('type')} {element.get('id')} | {name} | {location}")


def main(argv=None):
	argv = sys.argv[1:] if argv is None else argv
	if len(argv) < 2:
		print("Usage: python main.py KEY VALUE", file=sys.stderr)
		print("Example: python main.py tourism museum", file=sys.stderr)
		return 1

	key = argv[0]
	value = argv[1]
	limit = int(argv[2]) if len(argv) > 2 else DEFAULT_LIMIT
	query = build_query(key, value, limit)

	try:
		payload = fetch_overpass(query)
	except urllib.error.HTTPError as err:
		body = err.read().decode("utf-8", errors="replace")
		print(f"HTTP error: {err.code} {err.reason}", file=sys.stderr)
		if body.strip():
			print(body, file=sys.stderr)
		return 1
	except urllib.error.URLError as err:
		print(f"Connection error: {err.reason}", file=sys.stderr)
		return 1

	print_results(payload)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
