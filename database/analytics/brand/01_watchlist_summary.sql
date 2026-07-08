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

    b.brand_id,

    p.product_id,

    p.product_name,

    b.brand_name,

    COALESCE(ws.total_watchlists, 0) AS total_watchlists,

    COALESCE(ws.active_watchlists, 0) AS active_watchlists,

    ws.average_target_price,

    ps.current_average_price,

    ROUND(
        ps.current_average_price -
        ws.average_target_price,
        2
    ) AS price_gap

FROM products p

JOIN brands b
    ON p.brand_id = b.brand_id

LEFT JOIN (

    SELECT

        product_id,

        COUNT(*) AS total_watchlists,

        SUM(is_active = TRUE) AS active_watchlists,

        ROUND(
            AVG(current_target_price),
            2
        ) AS average_target_price

    FROM watchlists

    GROUP BY product_id

) ws

ON p.product_id = ws.product_id

LEFT JOIN (

    SELECT

        product_id,

        ROUND(
            AVG(price),
            2
        ) AS current_average_price

    FROM latest_prices

    GROUP BY product_id

) ps

ON p.product_id = ps.product_id;