import requests
import json
from typing import Dict

# connect to a "real" API

## Example: OpenWeatherMap
URL = "https://api.openweathermap.org/data/2.5/weather"

# TODO: get an API key from openweathermap.org and fill it in here!
API_KEY = "7e6d35ef8ad769a4d92a7c1169a9b9a5"

def get_weather(city) -> Dict:
    res = requests.get(URL, params={"q": city, "appid": API_KEY})
    return res.json()

# Trying another api for +2 points

f = r"https://official-joke-api.appspot.com/random_joke"

def get_joke(f):
	
     # uses the request library to make the api call
     # uses the json.loads to turn the data into a python dictionary
     data = requests.get(f)
     joke = json.loads(data.text)
     return joke


def main():
    
    # gets the joke using the official joke api
    # then displays it to user, as well as the joke's type.
    joke = get_joke(f)
    print(joke["type"])
    print(joke["setup"])
    print(joke["punchline"])
    
    print() # used to seperate the returns of 2 differet api calls.
    

    temp = get_weather("London")
    print(temp)

if __name__ == "__main__":
    main()