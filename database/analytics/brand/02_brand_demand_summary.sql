/*
==========================================================
IntentIQ

File: 02_brand_demand_summary.sql

Description:
Creates a brand-level demand summary for analytics.

Author: Arjun Sair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW brand_demand_summary AS

SELECT

    b.brand_id,

    b.brand_name,

    COUNT(DISTINCT p.product_id) AS total_products,

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
    ) AS average_market_price,

    ROUND(
        AVG(lp.price) -
        AVG(w.current_target_price),
        2
    ) AS average_price_gap

FROM brands b

JOIN products p
    ON b.brand_id = p.brand_id

LEFT JOIN watchlists w
    ON p.product_id = w.product_id

LEFT JOIN latest_prices lp
    ON p.product_id = lp.product_id

GROUP BY

    b.brand_id,

    b.brand_name;
    