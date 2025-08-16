import os
from dotenv import load_dotenv
import requests
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
API_KEY = os.environ.get("WEATHER_API_KEY", "d67ce18090984510989191413251008")  # fallback key

BASE_URL = "https://api.weatherapi.com/v1/current.json"

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://weather-app-salwa-kazmis-projects.vercel.app"],  # your Vercel frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create SQLite DB
conn = sqlite3.connect("weather.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    temperature REAL,
    description TEXT,
    date_time TEXT
)
""")
conn.commit()

# Weather endpoint
@app.get("/weather/{city}")
def get_weather(city: str):
    params = {"key": API_KEY, "q": city}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "error" in data:
        return {"error": data["error"]["message"]}

    city_name = data["location"]["name"]
    temp = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    description = data["current"]["condition"]["text"]
    icon = "https:" + data["current"]["condition"]["icon"]

    # Save to DB
    cursor.execute(
        "INSERT INTO history (city, temperature, description, date_time) VALUES (?, ?, ?, ?)",
        (city_name, temp, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()

    return {
        "city": city_name,
        "temperature": temp,
        "humidity": humidity,
        "description": description,
        "icon": icon
    }

# History endpoint
@app.get("/history")
def get_history():
    cursor.execute("SELECT city, temperature, description FROM history ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    history = [{"city": row[0], "temperature": row[1], "description": row[2]} for row in rows]
    return history
