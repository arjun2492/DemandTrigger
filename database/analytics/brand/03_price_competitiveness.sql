/*
==========================================================
IntentIQ

File: 03_price_competitiveness.sql

Description:
Creates a product-level pricing competitiveness view.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW price_competitiveness AS

SELECT

    cps.product_id,

    cps.product_name,

    cps.brand_name,

    cheapest.store_name AS cheapest_store,

    MIN(cps.current_price) AS cheapest_price,

    MAX(cps.current_price) AS highest_price,

    MAX(cps.current_price) - MIN(cps.current_price)
        AS price_difference,
    
    ROUND(

        (
            MAX(cps.current_price) -
            MIN(cps.current_price)
        )

        /

        MIN(cps.current_price)

        * 100,

        2

    ) AS price_difference_pct,

    COUNT(*) AS stores_available

FROM store_price_comparison cps

JOIN (

    SELECT

        product_id,

        MIN(current_price) AS min_price

    FROM store_price_comparison

    GROUP BY product_id

) lowest

ON cps.product_id = lowest.product_id

JOIN store_price_comparison cheapest

ON cheapest.product_id = lowest.product_id
AND cheapest.current_price = lowest.min_price

GROUP BY

    cps.product_id,

    cps.product_name,

    cps.brand_name,

    cheapest.store_name;
