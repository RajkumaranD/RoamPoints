def fetch_live_points(program, origin, destination):
    """
    Placeholder for future real-time API or scraper integration.
    For now, always return None.
    """
    # Example: If connected to Point.me or SeatSpy API, call it here
    return None

def get_estimated_points(program, origin, destination):
    route_key = f"{origin}-{destination}"

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
        # 1. Try real-time fetch (stub for future expansion)
        live_value = fetch_live_points(program, origin, destination)
        if live_value:
            return live_value
    except Exception as e:
        print(f"[ERROR] Fetching real-time points for {program}: {e}")

    # 2. Fallback to static chart
    if route_key in fallback_award_chart.get(program, {}):
        return fallback_award_chart[program][route_key]
    else:
        return -1
