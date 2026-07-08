/*
==========================================================
IntentIQ

File: 03_price_history_summary.sql

Description:
Creates a historical price view for trend analysis.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW price_history_summary AS

SELECT

    ph.price_id,

    b.brand_id,

    p.product_id,

    ph.store_id,

    p.product_name,

    b.brand_name,

    s.store_name,

    ph.price,

    DATE(ph.scraped_at) AS scrape_date,

    ph.scraped_at

FROM price_history ph

JOIN products p
    ON ph.product_id = p.product_id

JOIN brands b
    ON p.brand_id = b.brand_id

JOIN stores s
    ON ph.store_id = s.store_id

ORDER BY

    p.product_name,

    ph.scraped_at;