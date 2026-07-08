/*
==========================================================
IntentIQ

File: 02_dim_brands.sql

Description:
Creates the brand dimension view for Power BI.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW dim_brands AS

SELECT

    brand_id,

    brand_name

FROM brands;