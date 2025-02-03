import openmeteo_requests
import requests_cache
import psycopg2
import psycopg2.extras
from retry_requests import retry
from geopy.geocoders import Nominatim
from datetime import datetime, timezone, timedelta
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

engine = create_engine(f"postgresql+psycopg2://{"de11_asse"}:{"Tzm1WVWU"}@{"data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com"}:{"5432"}/{"pagila"}")


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_coordinates(location_name):
    """Fetch latitude and longitude for the given location."""
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    return None, None

def fetch_weather_data(latitude, longitude):
    """Fetch hourly weather forecast for the next 3 days."""
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
	"latitude": latitude,
	"longitude": longitude,
	"current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
	"hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "wind_speed_10m"],
	"daily": ["apparent_temperature_max", "apparent_temperature_min", "uv_index_max", "precipitation_hours"]
}

    responses = openmeteo.weather_api(url, params=params)
    if not responses:
        print("No API response received.")
        return []

    response = responses[0]


    #CREATING HOURLY WEATHER DATAFRAME
    hourly = response.Hourly()
    
    hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    )}
    
    hourly_data["temperature_2m"] = hourly.Variables(0).ValuesAsNumpy()
    hourly_data["relative_humidity_2m"] = hourly.Variables(1).ValuesAsNumpy()
    hourly_data["apparent_temperature"] = hourly.Variables(2).ValuesAsNumpy()
    hourly_data["precipitation"] = hourly.Variables(3).ValuesAsNumpy()
    hourly_data["wind_speed_10m"] = hourly.Variables(4).ValuesAsNumpy()
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    
    return hourly_dataframe


weather_data = fetch_weather_data(*get_coordinates('Tokyo, Japan'))
weather_data.to_sql('hourly_weather', engine, schema='student', if_exists='replace', index=False)
