# scrapers.py
# Real-time award mileage scraping functions for Delta and United

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime


def get_delta_award_miles(origin, destination, departure_date):
    formatted_date = datetime.strptime(departure_date, "%Y-%m-%d").strftime("%a %b %d %Y")
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # Add this line
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.delta.com/")

    try:
        wait = WebDriverWait(driver, 30)

        # Wait for modal to disappear
        try:
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "modal-container")))
        except:
            pass

        # Enter origin
        from_input = wait.until(EC.element_to_be_clickable((By.ID, "fromAirportName")))
        from_input.clear()
        from_input.send_keys(origin)
        time.sleep(2)
        from_suggestion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox'] li")))
        from_suggestion.click()

        # Enter destination
        to_input = wait.until(EC.element_to_be_clickable((By.ID, "toAirportName")))
        to_input.clear()
        to_input.send_keys(destination)
        time.sleep(2)
        to_suggestion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox'] li")))
        to_suggestion.click()

        # Shop with miles
        shop_with_miles_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='awardTravel']")))
        shop_with_miles_label.click()

        # Select date
        calendar_input = wait.until(EC.element_to_be_clickable((By.ID, "input_departureDate_1")))
        calendar_input.click()
        aria_label = formatted_date
        date_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@aria-label='{aria_label}']")))
        date_button.click()

        # Submit
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit")))
        submit_button.click()
        time.sleep(15)

        # Extract SkyMiles values
        all_elements = driver.find_elements(By.XPATH, "//*")
        miles_found = []
        for el in all_elements:
            try:
                text = el.text.strip()
                if "," in text and "miles" in text.lower():
                    val = int(text.replace(",", "").split()[0])
                    miles_found.append(val)
            except:
                continue

        return min(miles_found) if miles_found else None

    except Exception as e:
        print("Delta scraping error:", e)
        return None
    finally:
        driver.quit()


# Placeholder - will later be implemented with real scraping

def get_united_award_miles(origin, destination, departure_date):
    # Placeholder logic for now
    return 45000
