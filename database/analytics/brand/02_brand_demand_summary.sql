/*
==========================================================
IntentIQ

File: 02_brand_demand_summary.sql

Description:
Creates a brand-level demand summary for analytics.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW brand_demand_summary AS

SELECT

    b.brand_id,

    b.brand_name,

    COUNT(p.product_id) AS total_products,

    COALESCE(SUM(ws.total_watchlists), 0) AS total_watchlists,

    COALESCE(SUM(ws.active_watchlists), 0) AS active_watchlists,

    ROUND(
        AVG(ws.average_target_price),
        2
    ) AS average_target_price,

    ROUND(
        AVG(ps.current_average_price),
        2
    ) AS average_market_price,

    ROUND(
        AVG(ps.current_average_price) -
        AVG(ws.average_target_price),
        2
    ) AS average_price_gap

FROM brands b

JOIN products p
    ON b.brand_id = p.brand_id

LEFT JOIN (

    SELECT

        product_id,

        COUNT(*) AS total_watchlists,

        SUM(is_active = TRUE) AS active_watchlists,

        AVG(current_target_price) AS average_target_price

    FROM watchlists

    GROUP BY product_id

) ws

ON p.product_id = ws.product_id

LEFT JOIN (

    SELECT

        product_id,

        AVG(price) AS current_average_price

    FROM latest_prices

    GROUP BY product_id

) ps

ON p.product_id = ps.product_id

GROUP BY

    b.brand_id,

    b.brand_name;