def get_estimated_points(program, origin, destination):
    route_key = f"{origin}-{destination}"

    # Example of static fallback chart
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

    if route_key in fallback_award_chart.get(program, {}):
        return fallback_award_chart[program][route_key]
    else:
        return None