# RoamPoints Main App (with polished UI)
import streamlit as st
from datetime import datetime, timedelta
from award_charts import get_estimated_points
from utils import get_flight_price, evaluate_redemption

PROGRAMS = ["Delta", "United", "American Airlines", "Qatar Airways", "Virgin Atlantic"]
NEARBY_AIRPORTS = {
    "JFK": ["JFK", "LGA", "EWR", "PHL", "BOS"],
    "SFO": ["SFO", "OAK", "SJC", "SMF"],
    "ORD": ["ORD", "MDW", "MKE"]
}

# -------------------- SIDEBAR INPUTS --------------------
st.sidebar.header("🔍 Search Flight Redemption")
origin = st.sidebar.text_input("Origin Airport Code", "JFK")
destination = st.sidebar.text_input("Destination Airport Code", "LAX")
flight_date = st.sidebar.date_input("Departure Date", min_value=datetime.now() + timedelta(days=1))

search_radius = st.sidebar.radio(
    "Willing to drive for a cheaper flight?", [0, 100, 150, 200], index=0
)

if st.sidebar.button("Compare Programs"):
    st.session_state['trigger_search'] = True

# -------------------- HEADER --------------------
st.title("💰 RoamPoints: Flight Points vs Cash Evaluator")
st.markdown("### 🛫 Welcome to RoamPoints!")
st.write("RoamPoints helps you find out whether it's smarter to **redeem points** 🪙 or **pay cash** 💵 for your flights.")

with st.expander("📘 How RoamPoints Works"):
    st.markdown("""
    - ✅ Compare live cash prices via Amadeus
    - ✅ Estimate points required across airlines
    - ✅ See cost to buy points if needed
    - ✅ Get a recommendation: Use Points or Pay Cash
    """)

# -------------------- MAIN SEARCH LOGIC --------------------
if st.session_state.get('trigger_search'):
    airport_list = NEARBY_AIRPORTS.get(origin.upper(), [origin.upper()]) if search_radius > 0 else [origin.upper()]
    for airport_code in airport_list:
        st.markdown(f"---\n### ✈️ Results for Origin: `{airport_code}`")
        cash_price = get_flight_price(airport_code, destination.upper(), str(flight_date))

        if not cash_price:
            st.error(f"❌ Could not fetch flight price from {airport_code}.")
            continue

        st.metric(label="💵 Cash Price", value=f"${cash_price:.2f}")

        results = []
        for program in PROGRAMS:
            try:
                points = get_estimated_points(program, airport_code, destination.upper())

                if points == -1:
                    continue
                if not points:
                    st.warning(f"⚠️ No points returned for {program} from {airport_code}")
                    continue

                cpp, cost, savings, recommendation = evaluate_redemption(program, cash_price, points)

                results.append({
                    "Program": program,
                    "Points Required": points,
                    "Value/Point (¢)": float(cpp),
                    "Cost to Buy Points": f"${cost:.2f}",
                    "You Save": f"${savings:.2f}",
                    "Recommendation": recommendation
                })
            except Exception as e:
                st.error(f"Error evaluating {program}: {e}")
                continue

        if results:
            best_deal = min(results, key=lambda x: float(x["Value/Point (¢)"]))
            st.success(f"⭐ Best Deal: {best_deal['Program']} from `{airport_code}` — {best_deal['Value/Point (¢)']:.2f}¢/point")
            st.dataframe(results)
        else:
            st.warning(f"📭 No usable redemption data for `{airport_code}`.")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("🚀 Built with ❤️ by RoamPoints | Powered by Amadeus API")
# -------------------------------
# 🌍 EXPLORE DESTINATIONS BY POINTS
# -------------------------------
st.markdown("---")
st.markdown("## 🌍 Explore Destinations by Points You Have")

program_input = st.selectbox("Loyalty Program", PROGRAMS, key="explore_program")
points_available = st.number_input("How many points do you have?", min_value=1000, max_value=500000, step=1000, value=50000, key="explore_points")
explore = st.button("🔎 Show Where I Can Go")

AWARD_DESTINATIONS = {
    "Delta": {
        "JFK-LAX": 55000,
        "JFK-ATL": 25000,
        "JFK-MIA": 32000,
        "JFK-SEA": 60000,
        "JFK-AUS": 42000,
    },
    "United": {
        "JFK-ORD": 22000,
        "JFK-DEN": 35000,
        "JFK-SFO": 48000
    },
    "American Airlines": {
        "JFK-CLT": 20000,
        "JFK-MIA": 25000,
        "JFK-PHX": 50000
    }
}

if explore:
    matches = []
    routes = AWARD_DESTINATIONS.get(program_input, {})
    st.markdown(f"### ✈️ Destinations You Can Reach with `{points_available}` {program_input} Points:")

    for route, pts in routes.items():
        if pts <= points_available:
            origin, dest = route.split("-")
            cash_price = get_flight_price(origin, dest, str(flight_date))
            cpp = calculate_value_per_point(cash_price, pts) if cash_price else None

            matches.append({
                "Route": route,
                "Points Required": pts,
                "Cash Price": f"${cash_price:.2f}" if cash_price else "N/A",
                "Value/Point (¢)": f"{cpp:.2f}" if cpp else "N/A"
            })

    if matches:
        st.dataframe(matches)
    else:
        st.warning("😔 No routes found under your point limit.")

