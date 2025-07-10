def fetch_live_points(program, origin, destination):
    """
    Placeholder for future real-time API or scraper integration.
    For now, always return None — fallback will handle known routes.
    """
    return None

def get_estimated_points(program, origin, destination):
    route_key = f"{origin}-{destination}"

    fallback_award_chart = {
        "Delta": {
            "DFW-LGA": 55000,
            "DFW-JFK": 55000,
            "DFW-XNA": 30000,
            "JFK-DFW": 55000
        },
        "United": {
            "DFW-EWR": 50000,
            "DFW-ORD": 45000,
            "DFW-XNA": 25000
        },
        "American Airlines": {
            "DFW-LGA": 35000,
            "DFW-JFK": 35000,
            "DFW-XNA": 20000,
            "XNA-DFW": 20000
        },
        "Qatar Airways": {
            "DFW-DOH": 70000
        },
        "Virgin Atlantic": {
            "DFW-LHR": 47000
        }
    }

    try:
        live_value = fetch_live_points(program, origin, destination)
        if live_value:
            return live_value
    except Exception as e:
        print(f"[ERROR] Fetching real-time points for {program}: {e}")

    # Return fallback if available
    if route_key in fallback_award_chart.get(program, {}):
        return fallback_award_chart[program][route_key]
    else:
        return -1  # Route not supported — suppress warning
