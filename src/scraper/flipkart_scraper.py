"""
==========================================================
IntentIQ

File: flipkart_scraper.py

Description:
Scrapes Flipkart product listings and stores the results
in the raw_scrape_data table.

Author: Arjun S Nair
==========================================================
"""

import json
from datetime import datetime
from src.etl.raw_data_loader import insert_raw_scrape_data

from src.scraper.scraper_utils import (
    fetch_product_listings,
    create_browser,
    close_browser,
    validate_url,
    print_scrape_summary
)

# ==========================
# Scraper Functions
# ==========================

def scrape_product(page, listing):
    """
    Scrapes a single Flipkart product.
    """

    url = listing["product_url"]

    validate_url(url)

    page.goto(url)

    try:
        
        scripts = page.locator("script[type='application/ld+json']")  

        script = scripts.first.inner_text()      

        product_data = json.loads(script)[0]

        product_name = product_data["name"]

        current_price = product_data["offers"]["price"]

        currency = product_data["offers"]["priceCurrency"]

        availability_url = product_data["offers"]["availability"]

        if availability_url.endswith("InStock"):
            availability = "In Stock"

            scraper_status = "Success"
        
        else:
            availability = "Currently Unavailable"

            current_price = None

            scraper_status = "Price Not Available"

    except Exception as e:
        print(
            f"JSON-LD parsing failed for "
            f"{listing['retailer_product_name']}"
        )

        print(e)

        return {

            "listing_id": listing["listing_id"],
            "product_name": None,
            "current_price": None,
            "availability": "Unknown",
            "currency": "INR",
            "scraped_at": datetime.now(),
            "scraper_status": "Failed"

        }
    
    return {

        "listing_id": listing["listing_id"],
        "product_name": product_name,
        "current_price": current_price,
        "availability": availability,
        "currency": currency,
        "scraped_at": datetime.now(),
        "scraper_status": scraper_status
    }

# ==========================
# Main Pipeline
# ==========================

def main():
    
    listings = fetch_product_listings("Flipkart")

    success_count = 0
    unavailable_count = 0
    failed_count = 0

    playwright, browser, context, page = create_browser()

    try:
        
        for listing in listings:
            
            print(
                f"Now scraping: "
                f"{listing['retailer_product_name']}"
            )

            try:
                result = scrape_product(
                    page,
                    listing
                )

                insert_raw_scrape_data(result)

                print(
                    f"Scraped: "
                    f"{result['product_name']}"
                )

                if result["scraper_status"] == "Success":

                    success_count += 1

                elif result["scraper_status"] == "Price Not Available":

                    unavailable_count += 1
                    
                else:
                    failed_count += 1
            
            except Exception as e:
                
                failed_count += 1

                print(
                    f"Failed: "
                    f"{listing['retailer_product_name']}"
                )

                print(e)
    
    finally:
        
        close_browser(
            playwright,
            browser,
            context
        )
    
    print_scrape_summary(

        total=len(listings),

        success=success_count,

        unavailable=unavailable_count,

        failed=failed_count

    )

if __name__ == "__main__":
    main()
