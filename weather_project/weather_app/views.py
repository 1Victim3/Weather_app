import datetime
import requests

from django.shortcuts import render

def get_local_time(timezone):
    """
    Fetch local time for a given timezone using WorldTimeAPI.
    """
    try:
        url = f"http://worldtimeapi.org/api/timezone/{timezone}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data['datetime']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching time data: {e}")
        return None

# Create your views here.
def index(request):
    API_KEY = open("D:\\MicrosoftEdgeDownloads\\Weather\\weather_project\\API_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None
        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2,
        }
        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Fetching current weather data
    response = requests.get(current_weather_url.format(city, api_key)).json()

    # Get coordinates (latitude and longitude) for the forecast API
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(city, api_key)).json()

    # Fetch the timezone name using TimezoneDB API
    timezone_db_api_key = "03S93MKVSSPZ"  # Replace with your TimezoneDB API key
    timezone_name = get_timezone_name(lat, lon, timezone_db_api_key)

    # Current weather data
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),  # Convert from Kelvin to Celsius
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon'],
        "timezone": timezone_name  # Add timezone name to the weather data
    }

    # Fetch local time for the city using WorldTimeAPI
    local_time = get_local_time(weather_data['timezone'])
    weather_data['local_time'] = local_time  # Add local time to the weather data

    # Fetching daily summaries from the 5-day forecast (using hourly data)
    daily_forecasts = []
    daily_data = {}
    for forecast in forecast_response['list']:
        # Extract date (day) and temperature data
        dt = datetime.datetime.fromtimestamp(forecast['dt'])
        day = dt.strftime("%A")
        temp = round(forecast['main']['temp'] - 273.15, 2)

        if day not in daily_data:
            daily_data[day] = {"min_temp": temp, "max_temp": temp, "description": forecast['weather'][0]['description'],
                               "icon": forecast['weather'][0]['icon']}
        else:
            daily_data[day]["min_temp"] = min(daily_data[day]["min_temp"], temp)
            daily_data[day]["max_temp"] = max(daily_data[day]["max_temp"], temp)

    # Convert daily data to a list
    for day, data in daily_data.items():
        daily_forecasts.append({
            "day": day,
            "min_temp": data["min_temp"],
            "max_temp": data["max_temp"],
            "description": data["description"],
            "icon": data["icon"]
        })

    return weather_data, daily_forecasts

def get_timezone_name(lat, lon, api_key):
    """
    Fetch the timezone name for a given latitude and longitude using TimezoneDB API.
    """
    try:
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=position&lat={lat}&lng={lon}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data['zoneName']  # Returns the timezone name (e.g., "Asia/Kolkata")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching timezone data: {e}")
        return None
