import streamlit as st
import requests

POINT_PURCHASE_COST = {
    "United": 0.0175,
    "Delta": 0.013,
    "American Airlines": 0.014,
    "Qatar Airways": 0.018,
    "Virgin Atlantic": 0.015
}

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": st.secrets["API_KEY"],
        "client_secret": st.secrets["API_SECRET"]
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        st.error(f"Token Error: {response.text}")
    return response.json().get("access_token")

def get_flight_price(origin, destination, date):
    token = get_amadeus_token()
    if not token:
        st.error("Token generation failed")
        return None

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

    if response.status_code != 200:
        st.error(f"Flight Price API Error: {response.text}")
        return None

    if "data" in data and len(data["data"]) > 0:
        return float(data["data"][0]["price"]["total"])

    st.warning("No flight data found for given route/date.")
    return None

def calculate_value_per_point(cash_price, points):
    return round((cash_price / points) * 100, 2)

def evaluate_redemption(program, cash_price, points):
    point_price = POINT_PURCHASE_COST.get(program, 0.015)
    cost_to_buy = points * point_price
    savings = cash_price - cost_to_buy
    cpp = calculate_value_per_point(cash_price, points)

    if cost_to_buy < cash_price:
        recommendation = f"✅ Buy points & redeem (saves ${savings:.2f})"
    else:
        recommendation = "❌ Pay cash (buying points costs more)"

    return cpp, cost_to_buy, savings, recommendation