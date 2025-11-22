import requests

class PlacesAgent:
    def _overpass_query(self, lat, lon, radius=10000):
        query = f"""
        [out:json][timeout:60];
        (
          node["tourism"~"attraction|museum|zoo|theme_park"](around:{radius},{lat},{lon});
          node["leisure"="park"](around:{radius},{lat},{lon});
          node["historic"](around:{radius},{lat},{lon});
          way["tourism"~"attraction|museum|zoo|theme_park"](around:{radius},{lat},{lon});
          way["leisure"="park"](around:{radius},{lat},{lon});
          way["historic"](around:{radius},{lat},{lon});
        );
        out center tags;
        """
        resp = requests.post("https://overpass-api.de/api/interpreter", data=query, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def get_top_places(self, lat, lon, city, limit=6):
        try:
            data = self._overpass_query(lat, lon)
            elements = data.get("elements", [])
            noise_words = [
                "hotel", "guesthouse", "residency", "motel",
                "restaurant", "lodge", "school", "hostel", "dhaba"
            ]
            places_set = set()
            places = []
            for el in elements:
                tags = el.get("tags", {})
                name = tags.get("name")
                if not name:
                    continue
                lname = name.lower()
                if any(w in lname for w in noise_words):
                    continue
                if name not in places_set:
                    places.append(name)
                    places_set.add(name)
                if len(places) >= limit:
                    break
            if not places:
                return f"Sorry, there are no major tourist attractions listed for {city}."
            result = f"You can visit these top places in {city}:"
            for p in places:
                result += f"\n- {p}"
            return result
        except requests.HTTPError:
            return "Tourist places service returned an HTTP error."
        except Exception:
            return "Tourist places service is temporarily unavailable."
