import streamlit as st
import requests
from datetime import datetime
from datetime import timedelta

# -------------- CONFIG ---------------- #
API_KEY = st.secrets["5f9G91I35qQSsbIztIAbzAcrSzItH3Am"]
API_SECRET = st.secrets["ZDB0dhOydIQJJC5K"]

# Replace with your own or expand later
COMMON_AIRPORTS = {
    "JFK - New York (John F. Kennedy)": "JFK",
    "LHR - London (Heathrow)": "LHR",
    "SFO - San Francisco": "SFO",
    "ORD - Chicago (O'Hare)": "ORD",
    "LAX - Los Angeles": "LAX",
    "MAD - Madrid": "MAD",
    "DXB - Dubai": "DXB",
    "DEL - Delhi": "DEL",
    "SYD - Sydney": "SYD",
    "SIN - Singapore": "SIN"
}

PROGRAM_POINT_VALUES = {
    "United": 0.0175,
    "Delta": 0.013,
    "American Airlines": 0.014
}

AWARD_CHART = {
    "United": 45000,
    "Delta": 55000,
    "American Airlines": 50000
}

# -------------- AMADEUS FLIGHT PRICING ---------------- #

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
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
        return float(data["data"][0]["price"]["total"])
    else:
        return None

# -------------- LOGIC ---------------- #

def calculate_value_per_point(cash_price, points_used):
    return round((cash_price / points_used) * 100, 2)  # in cents

def evaluate(cash_price, points_used, point_price):
    cost_to_buy_points = points_used * point_price
    savings = cash_price - cost_to_buy_points
    value_per_point = calculate_value_per_point(cash_price, points_used)

    if cost_to_buy_points < cash_price:
        recommendation = f"✅ Buy points & redeem (saves ${savings:.2f})"
    else:
        recommendation = "❌ Pay cash (buying points costs more)"

    return cost_to_buy_points, savings, value_per_point, recommendation

# -------------- STREAMLIT UI ---------------- #

st.title("💰 Flight Points vs Cash Evaluator")

col1, col2 = st.columns(2)
with col1:
    origin_choice = st.selectbox("Origin Airport", list(COMMON_AIRPORTS.keys()))
with col2:
    destination_choice = st.selectbox("Destination Airport", list(COMMON_AIRPORTS.keys()))

origin = COMMON_AIRPORTS[origin_choice]
destination = COMMON_AIRPORTS[destination_choice]

flight_date = st.date_input("Departure Date", min_value=datetime.now() + timedelta(days=1))
program = st.selectbox("Loyalty Program", list(PROGRAM_POINT_VALUES.keys()))

# Autofill estimated points and price per point
points_required = AWARD_CHART.get(program)
point_price = PROGRAM_POINT_VALUES.get(program)

st.write(f"✳️ Estimated Points Required: **{points_required}**")
st.write(f"✳️ Estimated Point Purchase Price: **${point_price:.4f}/point**")

if st.button("Compare"):
    cash_price = get_flight_price(origin, destination, str(flight_date))
    if cash_price:
        cost, savings, cpp, recommendation = evaluate(cash_price, points_required, point_price)

        st.subheader("📊 Results")
        st.write(f"💸 Cash Price: **${cash_price:.2f}**")
        st.write(f"🪙 Cost to Buy Points: **${cost:.2f}**")
        st.write(f"💡 Value per Point: **{cpp:.2f}¢**")
        st.success(recommendation)
    else:
        st.error("Could not fetch flight price. Try a different route or future date.")
