import requests
from datetime import time, timedelta, datetime
import time
import schedule
import pytz
import json

with open("settings.json", "r") as f:
     settings = json.load(f)

# currentCity object is set to user-selected city, which is only a string
currentCity = settings["currentCity"]

# currentCity object is now accessing the key "cities" instead of the key
# "currentCity" (which was the user-selected city), and now we specify the "value"
# of the "key" which is what [currentCity] does (the value is the string)
currentCity = settings["cities"][currentCity]

lat = currentCity["lat"]
lon = currentCity["lon"]
timezone = pytz.timezone(currentCity["timezone"])
api_key = settings["apiKey"]
link = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&mode=json&units=metric&appid=" + api_key
degree_sign = u'\N{DEGREE SIGN}'
minsPerWeatherUpdate = 11

def getWeather():
        print("Obtaining weather data...\n")
        response = requests.get(link)
        temperature = response.json()['main']['temp']

        weatherFile = open("current_weather.txt", "w", encoding='utf-8')
        weatherFile.write(str(round(temperature)) + degree_sign + "C")
        weatherFile.close()
        print("Weather data acquisition completed.\n")

def getTime():
    print("Obtaining time...\n")
    now = datetime.now(timezone)
    current_time_hours = now.strftime("%I")
    current_time_minutes = now.strftime("%M")
    current_time_half = now.strftime("%p")
    current_time_hours = current_time_hours.lstrip('0')

    timeFile = open("current_time.txt", "w", encoding='utf-8')
    timeFile.write(current_time_hours + ":" + current_time_minutes + " " + current_time_half)
    timeFile.close()
    print("Time acquisition completed.\n")

getWeather()
getTime()

schedule.every().minute.at(":00").do(getTime)
schedule.every(minsPerWeatherUpdate).minutes.do(getWeather)

while True:
    schedule.run_pending()
    time.sleep(1)
