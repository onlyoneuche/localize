import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header
import requests

app = FastAPI()

# Load environment variables from the .env file (if present)
load_dotenv()
API_KEY = os.getenv("API_KEY")
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Function to get the city from the IP address using an IP geolocation API
def get_location_info(ip_address):
    ip_geolocation_url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(ip_geolocation_url)
    if response.status_code == 200:
        data = response.json()
        if data.get("bogon"):
            # return {
            #     "city": "Lagos",
            #     "lat": "6.4541",
            #     "lon": "3.3947"
            # }
            return None
        loc = data["loc"]
        coordinates = loc.split(",")
        lat, lon = coordinates[0], coordinates[1]
        return {
            "city": data.get("city", ""),
            "lat": lat,
            "lon": lon
        }
    return None


# Function to get weather information for a city
def get_temp(lat, lon):
    print("API KEY::::", API_KEY)
    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(weather_url)
    temp = 0
    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data["current"]["temp"] if weather_data["current"] else 0
        return temp
    return temp


@app.get("/api/hello")
async def say_hello(request: Request, x_real_ip: str = Header(None, alias='X-Real-IP')):
    print("X-Real-IP::::", x_real_ip)
    print("Request Host::::", request.client.host)
    visitor_name = request.query_params.get("visitor_name", "Guest")
    ip_address = x_real_ip if x_real_ip else request.client.host
    loc_res = get_location_info(ip_address)
    city = "Unknown"
    lat = 0
    lon = 0
    if loc_res is not None:
        city = loc_res["city"]
        lat = loc_res["lat"]
        lon = loc_res["lon"]

    temp = get_temp(lat, lon)

    greeting_success = f"Hello, {visitor_name.strip('"')}!, the temperature is {temp} degrees Celsius in {city.capitalize()}"
    greeting_failure = f"Sorry, {visitor_name.strip('"')}!, your location is {city} at this time"

    if city == "Unknown":
        message = greeting_failure
    else:
        message = greeting_success
    return {
        "client_ip": ip_address,
        "city": city.capitalize(),
        "greetings": message
    }
