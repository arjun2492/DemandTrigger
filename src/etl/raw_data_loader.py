from src.database.connection import get_connection

def insert_raw_scrape_data(scrape_result):
    """
    Inserts scraped data into the raw_scrape_data table.
    """
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO raw_scrape_data(
            listing_id,
            scraped_product_name,
            scraped_price,
            availability,
            scrape_status,
            scraped_at
        )
        VALUES(%s, %s, %s, %s, %s, %s)
    """

    values = (
        scrape_result["listing_id"],
        scrape_result["product_name"],
        scrape_result["current_price"],
        scrape_result["availability"],
        scrape_result["scraper_status"],
        scrape_result["scraped_at"]
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Raw scrape data inserted successfully.")

