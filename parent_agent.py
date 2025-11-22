import re
from agents.geocoding_agent import GeocodingAgent
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent

class TourismAgent:
    def __init__(self):
        self.geo = GeocodingAgent()
        self.weather = WeatherAgent()
        self.places = PlacesAgent()

    def _detect_place(self, text):
        """
        Extracts the best possible city/place name from the user's natural input.
        Works for inputs like 'I'm going to goa', 'places in bangalore', 'delhi weather'.
        Avoids extracting 'Going', 'What', or similar non-city phrases.
        """
        clean = re.sub(r"[^a-z\s]", " ", text.lower())
        ignore = set([
            "places", "go", "going", "i", "what", "how", "which", "to", "the", "is", "are", "can",
            "at", "in", "on", "visit", "weather", "temperature", "climate", "rain", "hot", "cold",
            "museum", "park", "see", "my", "let", "of", "for", "a", "am", "this", "that", "there",
            "here", "who", "whose", "and", "do", "does", "did", "me", "tell", "telll", "about", "you"
        ])
        words = [w for w in clean.split() if w]

        # Prefer window after prepositions "to", "in", "at" first
        for pre in ["to", "in", "at"]:
            if pre in words:
                idx = words.index(pre)
                for size in range(3, 0, -1):
                    phrase = " ".join(words[idx+1:idx+1+size]).strip()
                    if phrase and all(w not in ignore for w in phrase.split()):
                        coords = self.geo.get_coordinates(phrase)
                        if coords:
                            return (phrase.title(), coords)
                if idx+1 < len(words):
                    word = words[idx+1]
                    if word not in ignore:
                        coords = self.geo.get_coordinates(word)
                        if coords:
                            return (word.title(), coords)

        # Try all possible sliding windows, longest first
        MAX_CITY_WORDS = 3
        candidates = []
        for size in range(MAX_CITY_WORDS, 0, -1):
            for i in range(len(words) - size + 1):
                phrase = " ".join(words[i:i+size]).strip()
                phrase_words = phrase.split()
                if all(w in ignore for w in phrase_words):
                    continue
                if phrase_words and phrase_words[0] in ignore:
                    continue
                coords = self.geo.get_coordinates(phrase)
                if coords:
                    candidates.append((phrase.title(), coords))
        if candidates:
            return candidates[-1]
        # Fallback: try any single real word from end
        for w in reversed(words):
            if w not in ignore:
                coords = self.geo.get_coordinates(w)
                if coords:
                    return (w.title(), coords)
        return None, None

    def _detect_weather_intent(self, text):
        keywords = ["weather", "temperature", "climate", "rain", "hot", "cold", "snow"]
        return any(k in text.lower() for k in keywords)

    def _detect_places_intent(self, text):
        keywords = ["places", "attractions", "sights", "tourist", "visit", "museum", "park"]
        return any(k in text.lower() for k in keywords)

    def handle(self, message):
        place, coords = self._detect_place(message)
        if not place or not coords:
            return "I'm sorry, I couldn't recognize a valid city or place. Please check your input."
        lat, lon = coords
        wants_weather = self._detect_weather_intent(message)
        wants_places = self._detect_places_intent(message)
        output = []
        if wants_weather and not wants_places:
            output.append(self.weather.fetch_weather(lat, lon, place))
        elif wants_places and not wants_weather:
            output.append(self.places.get_top_places(lat, lon, place, limit=6))
        else:
            output.append(self.weather.fetch_weather(lat, lon, place))
            output.append(self.places.get_top_places(lat, lon, place, limit=6))
        return "\n".join(output)
