# main.py

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from scrapers import get_delta_award_miles, get_united_award_miles
from award_charts import get_estimated_points
from utils import get_flight_price, calculate_value_per_point, evaluate_redemption

PROGRAMS = ["Delta", "United", "American Airlines", "Qatar Airways", "Virgin Atlantic"]

st.title("💰 RoamPoints: Flight Points vs Cash Evaluator")

col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Origin Airport Code (e.g., JFK)", "JFK")
with col2:
    destination = st.text_input("Destination Airport Code (e.g., LAX)", "LAX")

flight_date = st.date_input("Departure Date", min_value=datetime.now() + timedelta(days=1))

if st.button("Compare Programs"):
    cash_price = get_flight_price(origin, destination, str(flight_date))

    if not cash_price:
        st.error("Could not fetch flight price. Try again.")
    else:
        st.write(f"💸 Cash price: **${cash_price:.2f}**")

        results = []
for program in PROGRAMS:
    # TEMPORARY: Skip real scraping, use estimated points for all programs
    points = get_estimated_points(program, origin, destination)

    if not points:
        continue

    cpp, cost, savings, recommendation = evaluate_redemption(program, cash_price, points)

    results.append({
        "Program": program,
        "Points Required": points,
        "Value/Point (¢)": cpp,
        "Cost to Buy Points": f"${cost:.2f}",
        "You Save": f"${savings:.2f}",
        "Recommendation": recommendation
    })

    if results:
            st.subheader("📊 Comparison Table")
            results_df = pd.DataFrame(results)

            # Find and tag best value deal
            best_index = results_df["Value/Point (¢)"].idxmax()
            results_df.loc[best_index, "Recommendation"] += " ⭐ Best Deal"

            # Sort by Value/Point descending
            results_df = results_df.sort_values(by="Value/Point (¢)", ascending=False)

            st.dataframe(results_df)
    else:
            st.warning("No program data available for this route/date.")
