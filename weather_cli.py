from weather import WeatherModel as Weather
# import air
import sys


weather = Weather(sys.argv[1:] if len(sys.argv) > 1 else input("Where are you located? "))

result = weather.fetchWeather()
if result > 0:
    print(str(result) + "mm of rain expected in " + weather.city[0] + " tomorrow!")
else:
    print("No rain in " + weather.city + " tomorrow!")

# air = air.AirModel(location)
# print(air.findCity())
