import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

<<<<<<< HEAD:Roampoints.py
# ----------------- CONFIG ----------------- #
=======
import streamlit as st

>>>>>>> 03157ce (Complete RoamPoints MVP with modular files and Streamlit app):points_vs_cash_app.py
API_KEY = st.secrets["API_KEY"]
API_SECRET = st.secrets["API_SECRET"]

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
    "Delta": 55000,
    "American Airlines": 50000
}

# ----------------- AMADEUS CASH PRICE ----------------- #
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

# ----------------- UNITED MILES SCRAPER ----------------- #
def get_united_award_miles(origin, destination, departure_date):
    url = f"https://www.united.com/en-us/flights/results?f={origin}&t={destination}&d={departure_date}&tt=1&sc=awardtravel"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        miles_text = soup.find_all(string=re.compile(r"\\d{1,3}(,\\d{3})*\\s+miles"))
        miles_cleaned = [int(re.search(r"(\\d{1,3}(?:,\\d{3})*)\\s+miles", t).group(1).replace(",", ""))
                         for t in miles_text if re.search(r"(\\d{1,3}(?:,\\d{3})*)\\s+miles", t)]
        return min(miles_cleaned) if miles_cleaned else None
    except Exception as e:
        return None

# ----------------- CALCULATIONS ----------------- #
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

# ----------------- STREAMLIT UI ----------------- #
st.title("💰 RoamPoints: Flight Points vs Cash Evaluator")

col1, col2 = st.columns(2)
with col1:
    origin_choice = st.selectbox("Origin Airport", list(COMMON_AIRPORTS.keys()))
with col2:
    destination_choice = st.selectbox("Destination Airport", list(COMMON_AIRPORTS.keys()))

origin = COMMON_AIRPORTS[origin_choice]
destination = COMMON_AIRPORTS[destination_choice]

flight_date = st.date_input("Departure Date", min_value=datetime.now() + timedelta(days=1))
program = st.selectbox("Loyalty Program", list(PROGRAM_POINT_VALUES.keys()))

point_price = PROGRAM_POINT_VALUES.get(program)

# Get points required
if program == "United":
    points_required = get_united_award_miles(origin, destination, str(flight_date)) or 45000
else:
    points_required = AWARD_CHART.get(program, 50000)

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
