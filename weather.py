import requests
import pandas as pd
from datetime import datetime, timedelta
import random

# Replace with your OpenWeatherMap API key
API_KEY = 'a9977b1fb16f24841529ac9a8b6051c9'

# List of cities
cities = ['New Delhi', 'Chandigarh', 'Tokyo', 'Toronto']

def fetch_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': city,
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description']
        }
    else:
        print(f"Failed to get weather data for {city}")
        return None

def predict_next_day_weather(today_temp):
    forecasted_temp = today_temp + random.uniform(-2, 2)
    return forecasted_temp

def fetch_forecast(city):
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(forecast_url, params=params)
    if response.status_code == 200:
        data = response.json()
        forecasted_data = data['list'][1]
        return forecasted_data['main']['temp'], forecasted_data['weather'][0]['description']
    else:
        print(f"Failed to get forecast data for {city}")
        return None, None

# Collect weather data
weather_data = [fetch_weather(city) for city in cities]

# Prepare data for CSV
rows = []
for data in weather_data:
    if data:
        temp_today = data['temperature']
        weather_today = data['weather']
        calculated_temp = predict_next_day_weather(temp_today)
        forecasted_temp, forecasted_weather = fetch_forecast(data['city'])
        rows.append({
            'City': data['city'],
            'Weather on Day 1': weather_today,
            'Forecasted Weather on Day 2': forecasted_weather,
            'Calculated Weather on Day 2': calculated_temp
        })

# Save to CSV
df = pd.DataFrame(rows)
df.to_csv('weather_forecast_comparison.csv', index=False)
print("CSV file created: weather_forecast_comparison.csv")
