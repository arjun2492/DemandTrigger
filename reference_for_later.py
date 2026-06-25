from playwright.sync_api import sync_playwright

from src.database.connection import get_connection

from datetime import datetime

import re

from src.etl.raw_data_loader import insert_raw_scrape_data

def fetch_product_listings():
    """
        Fetches Amazon product listings from the database.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            pl.listing_id,
            pl.product_id,
            pl.retailer_product_name,
            pl.product_url
        FROM 
            product_listings pl
        JOIN stores s
            ON pl.store_id = s.store_id
        WHERE
            s.store_name = 'Amazon';
    """

    cursor.execute(query)
    listings = cursor.fetchall()

    cursor.close()
    connection.close()

    return listings

def scrape_product(listing):
    """
        Opens an Amazon product page and prints its title.
    """

    url = listing["product_url"]

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless= False
        )
        
        page = browser.new_page()
        
        page.goto(url)

        page.wait_for_selector("span#productTitle", timeout=10000)

        product_name = (
             page
             .locator("span#productTitle")
             .inner_text()
             .replace("\u200b", "")
             .strip()
        )

        availability = (
             page
             .locator(".primary-availability-message")
             .inner_text()
             .strip()
        )

        if availability == "Currently unavailable.":
             current_price = None
             scraper_status = "Price Not Available"

        else:
             price_text = (
                  page
                  .locator("span.a-price-whole")
                  .first
                  .inner_text()
                  )
             
             current_price = int(re.sub(r"\D", "", price_text))

             scraper_status = "Success"


        browser.close()
        
        return {
             "listing_id": listing["listing_id"],
             "product_name": product_name,
             "current_price": current_price,
             "availability": availability,
             "currency": "INR",
             "scraped_at": datetime.now(),
             "scraper_status": scraper_status
             }
        
        

def main():
    
    listings = fetch_product_listings()
    # print(listings)

    for listing in listings[33:36]:
        
        print(f"Now scraping: {listing['retailer_product_name']}")
        
        try:
             result = scrape_product(listing)
             
             print(result)
             
             insert_raw_scrape_data(result)
             
             print(f"Scraped: {result['product_name']}")
        
        except Exception as e:
            print(f"Failed: {listing['retailer_product_name']}") 
            print(e)
    
if __name__ == "__main__":
        main()


