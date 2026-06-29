"""
==========================================================
IntentIQ

File: scraper_utils.py

Description:
Common utility functions shared by all retailer scrapers.

Author: Arjun S Nair
==========================================================
"""
from playwright.sync_api import sync_playwright

from src.database.connection import get_connection

def fetch_product_listings(store_name):
    """
    Fetches product listings for a given retailer.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query="""
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
            s.store_name = %s
            AND pl.listing_status = 'Active';
    """

    cursor.execute(query, (store_name,))

    listings = cursor.fetchall()

    cursor.close()
    connection.close()

    return listings

# ==========================
# Browser Functions
# ==========================

def create_browser(headless=False):
    """
    Creates a Playwright browser instance.
    """

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=headless
    )

    context = browser.new_context()

    page = context.new_page()

    return playwright, browser, context, page

def close_browser(playwright, browser, context):
    """
    Closes browser and Playwright session.
    """
    context.close()

    browser.close()

    playwright.stop()

# ==========================
# Validation Functions
# ==========================

def validate_url(url):
    """
    Ensures the URL is valid.
    """

    if not url.startswith("http"):

        raise ValueError(
            f"Invalid URL: {url}"
        )

# ==========================
# Logging Functions
# ==========================

def print_scrape_summary(
    total,
    success,
    unavailable,
    failed
):
    """
    Prints the scrape summary.
    """

    print("\n" + "=" * 40)

    print("SCRAPE SUMMARY")

    print("=" * 40)

    print(f"Total Listings      : {total}")

    print(f"Successful          : {success}")

    print(f"Price Unavailable   : {unavailable}")

    print(f"Failed              : {failed}")

    print("=" * 40)
