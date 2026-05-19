import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEETY_PRICES_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.environ.get("SHEETY_USERS_ENDPOINT")

class DataManager:

    def __init__(self):
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        self.customer_data = {}
        # FIXED: Added the missing attribute your get_customer_emails() method needs
        self.users_endpoint = SHEETY_USERS_ENDPOINT

    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    # This class is responsible for talking to the Google Sheet.
    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{row_id}",
            json=new_data,
            auth=self._authorization
        )

    # ADDED: This method resolves the AttributeError in main.py
    def update_destination_codes(self):
        """Loops through destination_data and updates the IATA codes in the Google Sheet."""
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )
            print(f"IATA Code update response status: {response.status_code}")

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, auth=self._authorization)
        data = response.json()
        # Name of spreadsheet 'tab' with the customer emails should be "users".
        self.customer_data = data["users"]
        return self.customer_data