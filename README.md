# ✈️ Automated Flight Price Tracker & Alert System

A Python-based automated financial engineering tool that monitors flight prices in real-time, updates a structured data backend, and alerts users when prices drop below their targeted thresholds. Built as part of the advanced Python curriculum journey.

---

## 🚀 Features

* **Automated Data Management:** Syncs directly with a Google Sheets backend via the Sheety API to manage target price entries and customer contact lists.
* **Object-Oriented Architecture:** Clean separation of concerns across dedicated modules for data routing, API compilation, and alerting.
* **Secure Environment Configurations:** Fully isolated API keys, endpoints, and authentication tokens using `python-dotenv`.
* **Local Caching:** Optimized execution workflows using localized caching to track data state efficiently.

---

## 📁 Project Structure

```text
├── .env                    # Local environment variables (Secret)
├── .gitignore              # Git exclusion configurations
├── data_manager.py         # Handles Sheety API interactions (GET/PUT)
├── flight_data.py          # Blueprint class for structuring flight metrics
├── flight_search.py        # Connects to Flight Search APIs to fetch live offers
├── main.py                 # Core application controller and execution loop
└── notification_manager.py # Manages automated user alert pipelines
⚙️ Setup & Installation
1. Clone the Repository
Bash
git clone [https://github.com/pavanhd360/day-39-flight-price.git](https://github.com/pavanhd360/day-39-flight-price.git)
cd day-39-flight-price
2. Set Up Virtual Environment
Bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
# Activate on macOS/Linux:
source .venv/bin/activate
3. Install Dependencies
Bash
pip install requests python-dotenv
4. Configure Environment Variables
Create a .env file in the root directory and add your secure API configurations:

Plaintext
SHEETY_USERNAME=your_username
SHEETY_PASSWORD=your_password
SHEETY_PRICES_ENDPOINT=[https://api.sheety.co/.../flightDeals/prices](https://api.sheety.co/.../flightDeals/prices)
SHEETY_USERS_ENDPOINT=[https://api.sheety.co/.../flightDeals/users](https://api.sheety.co/.../flightDeals/users)
(Note: Ensure your .env remains untracked in your local .gitignore file to safeguard credentials.)

📈 Execution
Run the primary automation sequence via the terminal:

Bash
python main.py
🛡️ License
Distributed under the MIT License. See LICENSE for more information.
