# lloyds_weather.py

import argparse
from urllib import parse, request, error
from configparser import ConfigParser
import json
import sys

OPENWEATHERMAP_API_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_openweathermap_api_key():
    """
    Get openweathermap api key from config file stored in a api_secret.ini file (not stored in
    version control since it's sensitive info
    :return: openweathermap api key
    """
    config = ConfigParser()
    config.read("api_secret.ini")
    return config["openweathermap"]["owm_api_key"]


def read_user_input():
    """
    Reads user input from the cli
    :return: arguments passed by the user
    """
    parser = argparse.ArgumentParser(description="User inputs city and OWM returns weather and temperature status")

    parser.add_argument("city", nargs="+", type=str, help="City name:")
    return parser.parse_args()


def create_weather_request(city):
    """Creates the full weather request URL

    Args:
        city (List[str]): Name of the city being passed as an input argument

    Returns:
        str: URL that makes a request to openweathermap for that given city
    """
    owm_api_key = get_openweathermap_api_key()
    city_name = " ".join(city)
    city_url = parse.quote_plus(city_name)
    url = f"{OPENWEATHERMAP_API_URL}?q={city_url}&appid={owm_api_key}"
    return url


def get_weather(request_url):
    """Creates an API request to the openweathermap api and returns a Python object.

    Args:
        request_url (str): City URL created for OpenWeather's city endpoint

    Returns:
        dict: Weather information for that specific city
    """
    try:
        response = request.urlopen(request_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:
            sys.exit("401: Access denied - Please check your API key is correct")
        elif http_error.code == 404:
            sys.exit("404: Not Found - Weather data could not be found for this city")
        else:
            sys.exit(f"Error occured. Could not process... ({http_error.code})")

    data = response.read()
    return json.loads(data)


def show_weather_details(weather_details):
    """Prints weather data for a given city in a human readable format

    Args:
        weather_details (dict): response from a call to openweatherapi
    """
    city = weather_details["name"]
    weather = weather_details["weather"][0]["description"]
    temp = weather_details["main"]["temp"]
    feels_like = weather_details["main"]["feels_like"]
    country = weather_details["sys"]["country"]

    print(f"City: {city}", end="")
    print(f"\t\tCountry: {country}", end="")
    print(f"\tWeather: {weather.capitalize()}", end=" ")
    print(f"\tTemperature: {temp}°C", end="")
    print(f"\tFeels like: {feels_like}°C")


if __name__ == '__main__':
    user_input = read_user_input()
    owm_request_url = create_weather_request(user_input.city)
    weather_data = get_weather(owm_request_url)
    show_weather_details(weather_data)
