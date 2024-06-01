import re
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import pandas as pd

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # page.goto("https://www.windsorsola.com/floorplans/a1?Beds=1&Baths=1&MaxSqft=1000")
    page.goto("https://www.windsorlantanahills.com/floorplans/a1?Beds=1&Baths=1&MaxSqft=1000")
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Close").click()
    # page.get_by_role("button", name="Floor Plans 1 floor plan").click()
    # page.get_by_text("A2", exact=True).click()
    # page.get_by_text("A2").click()
    # page.get_by_text("A3").click()
    # page.get_by_text("A5").click()
    # page.get_by_text("A6").click()
    # page.get_by_text("A7").click()
    # page.get_by_text("A8").click()
    # page.get_by_text("A9").click()
    # page.get_by_text("A10").click()
    # page.get_by_text("A11").click()
    # page.get_by_text("A12").click()
    # page.get_by_text("A13").click()
    # page.get_by_text("A14").click()
    # page.get_by_text("A15").click()
    # page.get_by_role("button", name="Floor Plans 14 floor plans").click()
    # page.wait_for_timeout(2000)
    page_content = page.content()
    with open("page_source.html", "w") as file:
        file.write(page_content)

    context.close()
    browser.close()

    parse_html("page_source.html")

def parse_html(file_path) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    # Initialize a list to store apartment data
    apartments = []
    # Find all table row elements in the tbody
    for row in soup.select("tr[data-selenium-id^='urow']"):
        # Extract the amenities as a list and then join them into a single string for better readability
        amenities_list = [
            li.get_text(strip=True)
            for li in row.select("td[data-selenium-id^='Amenity'] ul li")
        ]
        amenities_str = ', '.join(amenities_list)
        apartment = {
            "Apartment":
            row.select_one("td[data-selenium-id^='Apt']").get_text(strip=True),
            "Square Feet":
            row.select_one("td[data-selenium-id^='Sqft']").get_text(
                strip=True),
            "Rent":
            row.select_one("td[data-selenium-id^='Rent']").get_text(
                strip=True),
            "Amenities":
            amenities_str,
            "Available Date":
            row.select_one("td[data-selenium-id^='AvailDate']").get_text(
                strip=True)
        }
        apartments.append(apartment)
    # Convert the list to a DataFrame
    df = pd.DataFrame(apartments)
    print(df)
    df.to_csv('apartments_data.csv', index=False)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
