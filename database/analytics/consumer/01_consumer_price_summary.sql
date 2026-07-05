/*
==========================================================
IntentIQ

File: 01_consumer_price_summary.sql

Description:
Creates a consumer analytics view summarizing
the latest prices across all stores for every product.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW consumer_price_summary AS

SELECT
    p.product_id,

    p.product_name,

    b.brand_name,

    MIN(lp.price) AS lowest_price,

    MAX(lp.price) AS highest_price,

    ROUND(AVG(lp.price), 2) AS average_price,

    COUNT(lp.store_id) AS store_count

FROM products p

JOIN brands b
    ON p.brand_id = b.brand_id

JOIN latest_prices lp
    ON p.product_id = lp.product_id

GROUP BY
    p.product_id,

    p.product_name,

    b.brand_name;

