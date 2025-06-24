# RoamPoints Main App (Refined UI)
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

# Sidebar Inputs
st.sidebar.header("✈️ Flight Search Settings")
origin = st.sidebar.text_input("Origin Airport Code", "JFK")
destination = st.sidebar.text_input("Destination Airport Code", "LAX")
flight_date = st.sidebar.date_input("Departure Date", min_value=datetime.now() + timedelta(days=1))

search_radius = st.sidebar.radio(
    "How far are you willing to drive for a cheaper flight?",
    [0, 100, 150, 200],
    index=0
)

compare = st.sidebar.button("🔍 Compare Programs")

# Main UI
st.title("💰 RoamPoints: Flight Points vs Cash Evaluator")
st.markdown("""
RoamPoints helps you quickly figure out whether it's better to **redeem points** 🪙 or **pay cash** 💵 for a flight.

---

""")

if compare:
    try:
        st.markdown("### 🚦 Searching for best flight options...")

        airport_list = NEARBY_AIRPORTS.get(origin.upper(), [origin.upper()]) if search_radius > 0 else [origin.upper()]
        for airport_code in airport_list:
            st.markdown(f"---\n### 🛫 Origin: `{airport_code}`")

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
                        continue  # Route unsupported, silently skip
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
                    st.error(f"⚠️ Error evaluating {program}: {e}")
                    continue

            if results:
                best_deal = min(results, key=lambda x: float(x["Value/Point (¢)"]))
                st.success(
                    f"⭐ Best Deal: **{best_deal['Program']}** from `{airport_code}` — "
                    f"**{best_deal['Value/Point (¢)']:.2f}¢/point**"
                )
                st.dataframe(results)
            else:
                st.warning(f"📭 No usable redemption data for `{airport_code}`.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
