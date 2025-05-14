import requests
import streamlit as st
import random

# Simulated cash price variance per airport
CASH_VARIANCE = {
    "LGA": (10, 40),
    "EWR": (-20, 10),
    "PHL": (20, 60),
    "BOS": (-15, 30),
}

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": st.secrets["API_KEY"],
        "client_secret": st.secrets["API_SECRET"]
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

def get_flight_price(origin, destination, date):
    token = get_amadeus_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1,
        "currencyCode": "USD",
        "max": 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        base_price = float(data["data"][0]["price"]["total"])

        # Apply randomized adjustment for alternate airports
        if origin in CASH_VARIANCE:
            offset = random.uniform(*CASH_VARIANCE[origin])
            return round(base_price + offset, 2)

        return base_price
    else:
        return None

def calculate_value_per_point(cash_price, points_used):
    return round((cash_price / points_used) * 100, 2) if points_used else 0

def evaluate_redemption(program, cash_price, points_used):
    PROGRAM_POINT_VALUES = {
        "United": 0.0175,
        "Delta": 0.013,
        "American Airlines": 0.014,
        "Qatar Airways": 0.015,
        "Virgin Atlantic": 0.015
    }

    point_price = PROGRAM_POINT_VALUES.get(program, 0.014)
    cost_to_buy = points_used * point_price
    savings = cash_price - cost_to_buy
    value_per_point = calculate_value_per_point(cash_price, points_used)

    if cost_to_buy < cash_price:
        recommendation = f"✅ Buy points & redeem (saves ${savings:.2f})"
    else:
        recommendation = "❌ Pay cash (buying points costs more)"

    return value_per_point, cost_to_buy, savings, recommendation
