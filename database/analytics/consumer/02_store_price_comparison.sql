/*
==========================================================
IntentIQ

File: 02_store_price_comparison.sql

Description:
Creates a store-wise comparison of the latest
available prices for every product.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW store_price_comparison AS

SELECT
    b.brand_id,

    p.product_id,

    lp.store_id,

    p.product_name,

    b.brand_name,

    s.store_name,

    lp.price AS current_price,

    lp.scraped_at

FROM latest_prices lp

JOIN products p
    ON lp.product_id = p.product_id

JOIN brands b
    ON p.brand_id = b.brand_id

JOIN stores s
    ON lp.store_id = s.store_id

ORDER BY

    p.product_name,

    current_price;

    