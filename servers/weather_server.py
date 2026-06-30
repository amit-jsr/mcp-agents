# ============================================================
# TRANSPORT 2: streamable-http
# Runs as a standalone HTTP server — client hits it via URL
# Start with: python weather_server.py
# Runs on: http://localhost:8000/mcp
# ============================================================

from fastmcp import FastMCP
import random

mcp = FastMCP("WeatherExpert")

# Simulated weather data (replace with real API call if needed)
WEATHER_DATA = {
    "delhi": {"temp": 38, "condition": "Sunny", "humidity": 45},
    "mumbai": {"temp": 32, "condition": "Humid", "humidity": 85},
    "bangalore": {"temp": 24, "condition": "Cloudy", "humidity": 70},
    "kolkata": {"temp": 35, "condition": "Partly Cloudy", "humidity": 75},
    "london": {"temp": 15, "condition": "Rainy", "humidity": 90},
    "new york": {"temp": 22, "condition": "Clear", "humidity": 55},
}

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get current weather for a city"""
    key = city.lower()
    if key in WEATHER_DATA:
        data = WEATHER_DATA[key]
        return {
            "city": city,
            "temperature_celsius": data["temp"],
            "condition": data["condition"],
            "humidity_percent": data["humidity"]
        }
    # Fallback for unknown cities
    return {
        "city": city,
        "temperature_celsius": random.randint(15, 40),
        "condition": random.choice(["Sunny", "Cloudy", "Rainy"]),
        "humidity_percent": random.randint(40, 90)
    }

@mcp.tool()
def compare_weather(city1: str, city2: str) -> str:
    """Compare weather between two cities"""
    w1 = get_weather(city1)
    w2 = get_weather(city2)
    hotter = city1 if w1["temperature_celsius"] > w2["temperature_celsius"] else city2
    return (
        f"{city1}: {w1['temperature_celsius']}°C, {w1['condition']}\n"
        f"{city2}: {w2['temperature_celsius']}°C, {w2['condition']}\n"
        f"→ {hotter} is hotter"
    )

if __name__ == "__main__":
    # STREAMABLE-HTTP: runs as a web server, client connects via URL
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
