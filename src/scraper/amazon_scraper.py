from playwright.sync_api import sync_playwright

from src.database.connection import get_connection

from datetime import datetime

import re

from src.etl.raw_data_loader import insert_raw_scrape_data

def fetch_product_listings(store_name):
    """
        Fetches product listings of a given store.
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
            s.store_name = %s;
    """

    cursor.execute(query, (store_name,))
    listings = cursor.fetchall()

    cursor.close()
    connection.close()

    return listings

def scrape_product(page, listing):
    """
        Opens an Amazon product page and prints its title.
    """

    url = listing["product_url"]
    
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

        try:
            price_text = (
                page
                .locator("span.a-price-whole")
                .first
                .inner_text()
                )
            
            current_price = int(re.sub(r"\D", "", price_text))
            
            scraper_status = "Success"
        
        except Exception as e:
            
            print(f"Price extraction failed for {listing['retailer_product_name']}")

            print(e)

            current_price = None

            scraper_status = "Price Not Available"
            
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
    
    listings = fetch_product_listings("Amazon")
    
    success_count = 0
    unavailable_count = 0
    failed_count=0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        
        for listing in listings:
            
            print(f"Now scraping: {listing['retailer_product_name']}")
            
            try:
             result = scrape_product(page, listing)
             
             insert_raw_scrape_data(result)

             if(result["scraper_status"]=="Success"):
                 success_count += 1

             else:
                 unavailable_count += 1
             
             print(f"Scraped: {result['product_name']}")
             
            except Exception as e:
                failed_count += 1
                print(f"Failed: {listing['retailer_product_name']}")
                print(f"URL:{listing['product_url']}")
                print(e)
        
        browser.close()
    
    print("==============================")

    print("\nAmazon Scrape Summary")

    print("==============================")

    print(f"{'Total Lisitngs':<20}: {len(listings)}")

    print(f"{'Successful':<20}: {success_count}")

    print(f"{'Price Unvailable':<20}: {unavailable_count}")

    print(f"{'Failed':<20}: {failed_count}")

    print("==============================")
    
if __name__ == "__main__":
        main()


