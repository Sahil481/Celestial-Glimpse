import requests
import json
from datetime import datetime
import os

api_key = os.environ["APIKEY"]

class APOD:
    def __init__(self):
        response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
        data = json.loads(response.content)
        self.date = self.striptime(data)
        self.title = data["title"]
        self.desc = data["explanation"]
        self.image = data["hdurl"]

    def striptime(self, data):
        current_apod_date = data["date"]
        current_date_data = datetime.strptime(current_apod_date, "%Y-%m-%d")
        return current_date_data
