import requests

class GeocodingAgent:
    def get_coordinates(self, location):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location,
            "format": "json",
            "countrycodes": "IN",
            "limit": 1
        }
        headers = {"User-Agent": "AI-Tourism-Agent-Project"}
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            if len(data) == 0:
                return None
            return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception:
            return None
