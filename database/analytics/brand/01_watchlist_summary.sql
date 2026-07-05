/*
==========================================================
IntentIQ

File: 01_watchlist_summary.sql

Description:
Creates a brand analytics view summarizing
watchlist demand and target prices.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW watchlist_summary AS

SELECT

    p.product_id,

    p.product_name,

    b.brand_name,

    COUNT(w.watchlist_id) AS total_watchlists,

    SUM(
        CASE
            WHEN w.is_active = TRUE
            THEN 1
            ELSE 0
        END
    ) AS active_watchlists,

    ROUND(
        AVG(w.current_target_price),
        2
    ) AS average_target_price,

    ROUND(
        AVG(lp.price),
        2
    ) AS current_average_price,

    ROUND(
        AVG(lp.price) - AVG(w.current_target_price),
        2
    ) AS price_gap

FROM products p

JOIN brands b
    ON p.brand_id = b.brand_id

LEFT JOIN watchlists w
    ON p.product_id = w.product_id

LEFT JOIN latest_prices lp
    ON p.product_id = lp.product_id

GROUP BY

    p.product_id,

    p.product_name,

    b.brand_name;