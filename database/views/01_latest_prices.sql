/*
==========================================================
IntentIQ

File: 01_latest_prices.sql

Description:
Fetches the latest price of watchlisted product.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW latest_prices AS 

SELECT
    ph1.price_id,
    ph1.product_id,
    ph1.store_id,
    ph1.price,
    ph1.scraped_at
FROM
    price_history ph1
JOIN
(
    SELECT
        product_id,
        store_id,
        MAX(scraped_at) AS latest_scrape

    FROM
        price_history

    GROUP BY
        product_id,
        store_id
) latest
ON ph1.product_id = latest.product_id
AND ph1.store_id = latest.store_id
AND ph1.scraped_at = latest.latest_scrape;

