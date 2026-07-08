/*
==========================================================
IntentIQ

File: 03_dim_stores.sql

Description:
Creates the store dimension view for Power BI.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

CREATE OR REPLACE VIEW dim_stores AS

SELECT

    store_id,

    store_name

FROM stores;