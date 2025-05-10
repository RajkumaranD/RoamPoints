# RoamPoints Main App
import streamlit as st
from datetime import datetime, timedelta
from award_charts import get_estimated_points
from utils import get_flight_price, calculate_value_per_point, evaluate_redemption

PROGRAMS = ["Delta", "United", "American Airlines", "Qatar Airways", "Virgin Atlantic"]

NEARBY_AIRPORTS = {
    "JFK": ["JFK", "LGA", "EWR", "PHL", "BOS"],
    "SFO": ["SFO", "OAK", "SJC", "SMF"],
    "ORD": ["ORD", "MDW", "MKE"]
}

st.title("💰 RoamPoints: Flight Points vs Cash Evaluator")

st.markdown("""
# ✈️ Welcome to RoamPoints!

RoamPoints helps you find out whether it's smarter to **redeem points** 🪙 or **pay cash** 💵 for your flights.

✅ Compare live cash prices via Amadeus  
✅ Estimate points required across airlines (Delta, United, AA, Qatar, Virgin Atlantic)  
✅ See cost to buy points if needed  
✅ Get a recommendation: **Use Points** or **Pay Cash**

---
""")

col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Origin Airport Code (e.g., JFK)", "JFK")
with col2:
    destination = st.text_input("Destination Airport Code (e.g., LAX)", "LAX")

flight_date = st.date_input("Departure Date", min_value=datetime.now() + timedelta(days=1))

st.markdown("""
---
### 🚗 Optional: Expand Search Radius
If you're open to flying out of nearby airports, select how far you're willing to drive below:
""")

search_radius = st.radio("How far are you willing to drive for a cheaper flight?", [0, 100, 150, 200], index=0)

if st.button("Compare Programs"):
    try:
        airport_list = NEARBY_AIRPORTS.get(origin.upper(), [origin.upper()]) if search_radius > 0 else [origin.upper()]

        all_results = []

        for airport_code in airport_list:
            st.subheader(f"Results for Origin: {airport_code}")
            cash_price = get_flight_price(airport_code, destination.upper(), str(flight_date))

            if not cash_price:
                st.error(f"Could not fetch flight price from {airport_code}.")
                continue

            st.write(f"💸 Cash price from {airport_code}: **${cash_price:.2f}**")

            results = []

            st.write(f"🔍 Checking programs for {airport_code}: {PROGRAMS}")
        for program in PROGRAMS:
                points = get_estimated_points(program, airport_code, destination.upper())
                if not points:
                    st.warning(f"No points returned for {program} from {airport_code}")
                    continue

                if not points:
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

            if results:
                # Highlight the best value/point result
                best_deal = min(results, key=lambda x: float(x["Value/Point (¢)"]))
                st.success(f"⭐ Best Deal Here: {best_deal['Program']} from {airport_code} — {float(best_deal['Value/Point (¢)']):.2f}¢/point")
                st.dataframe(results)
            else:
                st.warning(f"No program data available for airport {airport_code}.")

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")