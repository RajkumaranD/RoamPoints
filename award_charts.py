import random

# Simulated point variance per origin (nearby airports)
POINT_VARIANCE = {
    "LGA": (-2000, 4000),
    "EWR": (-3000, 3000),
    "PHL": (0, 7000),
    "BOS": (-1500, 5000),
}

def get_estimated_points(program, origin, destination):
    route_key = f"{origin}-{destination}"

    # Normalize to main metro area (e.g., all NYC airports → JFK)
    metro_origin = "JFK" if origin in ["LGA", "EWR", "PHL", "BOS"] else origin
    normalized_key = f"{metro_origin}-{destination}"

    # Static fallback chart
    fallback_award_chart = {
        "Delta": {
            "JFK-LAX": 55000,
            "JFK-SFO": 55000,
            "JFK-ORD": 25000,
        },
        "United": {
            "JFK-LAX": 45000,
            "JFK-SFO": 45000,
            "JFK-ORD": 22000,
        },
        "American Airlines": {
            "JFK-LAX": 50000,
            "JFK-SFO": 50000,
            "JFK-ORD": 20000,
        },
        "Qatar Airways": {
            "JFK-DOH": 70000
        },
        "Virgin Atlantic": {
            "JFK-LHR": 47000
        }
    }

    try:
        base_points = fallback_award_chart.get(program, {}).get(normalized_key)
        if base_points:
            # Apply random variation if from nearby alternate airport
            if origin in POINT_VARIANCE:
                offset = random.randint(*POINT_VARIANCE[origin])
                return max(10000, base_points + offset)
            return base_points
    except Exception as e:
        print(f"[ERROR] fallback lookup for {program}: {e}")

    return -1  # Suppress warning if route not supported
