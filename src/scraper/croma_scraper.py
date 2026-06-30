"""
==========================================================
IntentIQ

File: croma_scraper.py

Description:
Scrapes Croma product listings and stores the results
in the raw_scrape_data table.

Author: Arjun S Nair
==========================================================
"""
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
    Scrapes a single Croma product.
    """
    url = listing["product_url"]

    validate_url(url)
    page.goto(url)

    # --------------------------
    # Product Name
    # --------------------------

    product_name = (
        page
        .locator("h1.pd-title")
        .inner_text()
        .strip()
    )

    # --------------------------
    # Availability
    # --------------------------

    page_text = page.inner_text("body")

    if "Add to Cart" in page_text:
        availability = "In Stock"
        scraper_status = "Success"

        try:
            price_text = (
                page
                .locator("#pdp-product-price")
                .get_attribute("value")
            )

            current_price = int(float(price_text))

        except Exception:

            current_price = None

            scraper_status = "Price Not Available"
    
    else:
        availability = "Currently Unavailable"

        current_price = None

        scraper_status = "Price Not Available"

    return {
        "listing_id": listing["listing_id"],

        "product_name": product_name,

        "current_price": current_price,

        "currency": "INR",

        "availability": availability,

        "scraped_at": datetime.now(),

        "scraper_status": scraper_status
    }

   
# ==========================
# Main Pipeline
# ==========================

def main():

    listings = fetch_product_listings("Croma")

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

                else:

                    unavailable_count += 1

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










