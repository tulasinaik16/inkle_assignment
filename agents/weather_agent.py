import requests

class WeatherAgent:
    def fetch_weather(self, lat, lon, city):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "precipitation_probability",
            "timezone": "Asia/Kolkata",
            "temperature_unit": "celsius"
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            weather = data.get("current_weather", {})
            temp = weather.get("temperature")
            rain_chance = None
            if data.get("hourly") and data["hourly"].get("precipitation_probability"):
                rain_list = data["hourly"]["precipitation_probability"]
                if rain_list:
                    rain_chance = max(rain_list[:4])
            if temp is None:
                return f"Sorry, I couldn't fetch weather data for {city}."
            if rain_chance is not None:
                return f"Currently, the temperature in {city} is {temp}°C with a {rain_chance}% chance of rain."
            else:
                return f"Currently, the temperature in {city} is {temp}°C."
        except Exception:
            return "Weather service is temporarily unavailable."
