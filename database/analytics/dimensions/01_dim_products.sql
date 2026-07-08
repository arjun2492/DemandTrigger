/*
==========================================================
IntentIQ

File: 01_dim_products.sql

Description:
Creates the product dimension view for Power BI.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW dim_products AS

SELECT

    p.product_id,

    p.product_name,

    b.brand_id,

    b.brand_name

FROM products p

JOIN brands b
    ON p.brand_id = b.brand_id;