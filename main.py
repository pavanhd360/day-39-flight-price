import requests_cache
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# ==================== Conserve requests and preserve your free plan ====================
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    }
)
# ==================== Setup ====================
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Update destination codes if they are missing in the sheet
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Retrieve your customer emails ====================
customer_data = data_manager.get_customer_emails()
# Verify the name of your email column in your sheet. Yours may be different from mine
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]
# pprint(f"Your email list includes {customer_email_list}")

# ==================== Set the Dates and Origin Airport ====================
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
ORIGIN_CITY_IATA = "LHR"  # London Heathrow

# ==================== Find and Notify via SMS and Email ====================

for destination in sheet_data:
    pprint(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))
    pprient_price = cheapest_flight.price if cheapest_flight else "N/A"
    pprint(f"{destination['city']}: GBP {pprient_price}")

    # Ensure a flight object was returned and a valid price exists
    if cheapest_flight and cheapest_flight.price != "N/A":

        # Check if the found price is lower than the price stored in your Google Sheet
        if float(cheapest_flight.price) < float(destination["lowestPrice"]):
            pprint(f"New Record Low! Updating Sheet for {destination['city']}.")
            data_manager.update_lowest_price(destination["id"], cheapest_flight.price)
            destination["lowestPrice"] = cheapest_flight.price

            # 1. CREATE THE MESSAGE VARIABLE FIRST
        message = (f"Flight Price Update: GBP {cheapest_flight.price} to fly "
                   f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                   f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")

        # 2. TRIGGER THE SMS USING THE CREATED VARIABLE
        notification_manager.send_sms(message_body=message)

        # 3. TRIGGER THE EMAIL BATCH USING THE SAME VARIABLE
        if customer_email_list:
            pprint(f"Sending emails to {len(customer_email_list)} subscribers...")
            notification_manager.send_emails(email_list=customer_email_list, email_body=message)
        else:
            pprint("No customer emails found to notify.")

    else:
        pprint(f"No flights found for {destination['city']} today.")