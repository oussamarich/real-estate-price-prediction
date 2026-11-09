import requests  # To send HTTP requests to the website
from bs4 import BeautifulSoup  # To parse HTML content
import pandas as pd  # To store and manipulate the data
import time  # To pause between requests

def scrape_ads(max_ads=200):  # Function to scrape real estate ads with an optional limit
    base_url = "https://www.mubawab.ma/fr/sc/appartements-a-vendre?page={}"  # Base URL with page formatting
    headers = {"User-Agent": "Mozilla/5.0"}  # Header to mimic a real browser

    listings = []  # List to store all ad data
    page = 1  # Start from page 1
    count = 0  # Counter to keep track of how many ads have been scraped

    # Loop until we collect the required number of ads
    while count < max_ads:
        url = base_url.format(page)  # Construct full URL for current page
        response = requests.get(url, headers=headers)  # Send GET request
        soup = BeautifulSoup(response.content, "html.parser")  # Parse the HTML content
        ads = soup.find_all("div", class_="listingBox")  # Find all ad boxes

        if not ads:  # If no ads found, break the loop
            break

        for ad in ads:  # Loop through each ad on the page
            if count >= max_ads:  # If we've reached our target, stop scraping
                break
            try:
                # Extract title, price, location and other details
                title = ad.find("h2", class_="listingTit col-11")  # Title element
                price = ad.find("span", class_="priceTag hardShadow float-left")  # Price element
                location = ad.find("span", class_="listingH3")  # Location element
                detail_spans = ad.find_all("div", class_="adDetailFeature")  # List of detail items

                # Extract each detail, or set to None if not available
                surface = detail_spans[0].get_text(strip=True) if len(detail_spans) >= 1 else None
                rooms = detail_spans[1].get_text(strip=True) if len(detail_spans) >= 2 else None
                bedrooms = detail_spans[2].get_text(strip=True) if len(detail_spans) >= 3 else None
                bathroom = detail_spans[3].get_text(strip=True) if len(detail_spans) >= 4 else None

                # Append the ad data as a dictionary
                listings.append({
                    "Title": title.get_text(strip=True) if title else "",  # Get title text or empty
                    "Price": price.get_text(strip=True) if price else "",  # Get price text or empty
                    "Location": location.get_text(strip=True) if location else "",  # Get location or empty
                    "Surface": surface,  # Surface area text
                    "Rooms": rooms,  # Number of rooms text
                    "Bedrooms": bedrooms,  # Bedrooms text
                    "Bathroom": bathroom  # Bathrooms text
                })

                count += 1  # Increment the ad count
            except Exception as e:
                continue  # Skip this ad if any error occurs

        page += 1  # Move to the next page
        time.sleep(1)  # Pause 1 second to avoid overloading the server

    return pd.DataFrame(listings)  # Return the final list as a DataFrame
