# award_charts.py
# Estimated point values for programs without real-time scraping yet

def get_estimated_points(program, origin, destination):
    # Rough estimates based on common one-way redemptions
    estimates = {
        "American Airlines": 50000,        # Domestic/short-haul average
        "Qatar Airways": 70000,           # Economy long-haul (e.g., US to Doha)
        "Virgin Atlantic": 45000          # East Coast to London zone 5
    }
    return estimates.get(program, None)
