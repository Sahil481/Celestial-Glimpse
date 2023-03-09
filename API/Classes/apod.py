import requests
import json
from datetime import datetime
import os

# API key
api_key = os.getenv("APIKEY")

# This class handles the api call
class APOD:
    def __init__(self):
        # Fetching the Data from the NASA API
        response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
        data = json.loads(response.content)
        # Parsing and storing the JSON file
        self.date = self.striptime(data)
        self.title = data["title"]
        self.desc = data["explanation"]
        self.image = data["hdurl"]

    # Stripping the string into year-month-date format
    def striptime(self, data):
        current_apod_date = data["date"]
        current_date_data = datetime.strptime(current_apod_date, "%Y-%m-%d")
        return current_date_data
