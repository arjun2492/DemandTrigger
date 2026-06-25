from src.database.connection import get_connection

def fetch_raw_scrape_data():
    """
    Fetches valid raw scrape data for loading into price_history 
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            rsd.listing_id,
            rsd.scraped_price,
            rsd.scraped_at,
            pl.product_id,
            pl.store_id
        FROM raw_scrape_data as rsd
        JOIN product_listings as pl
            ON rsd.listing_id = pl.listing_id
        WHERE rsd.scraped_price IS NOT NULL
        AND rsd.scrape_status = 'Success';
    """

    cursor.execute(query)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records

def load_price_history(records):
    """
    Loads transformed records into price_history.
    """
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT IGNORE INTO price_history(
            product_id,
            store_id,
            price,
            scraped_at
            )
            VALUES(%s, %s, %s, %s)
    """
    values = [
        (
            record["product_id"],
            record["store_id"],
            record["scraped_price"],
            record["scraped_at"]
        )
        for record in records
    ]

    cursor.executemany(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print(f"Inserted {len(values)} records into price_history.")

def main():
    records = fetch_raw_scrape_data()

    print(f"Found {len(records)} records.")

    load_price_history(records)


if __name__ == "__main__":
    main()