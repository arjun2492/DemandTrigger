# IntentIQ Analytics Layer

## Overview

The Analytics Layer provides business-ready SQL views that power the IntentIQ dashboards.

Instead of querying transactional tables directly, reporting tools such as Power BI connect to these views to ensure consistent, reusable, and simplified analytics.

---

# Structure

```
analytics/

├── consumer/
│   ├── 01_consumer_price_summary.sql
│   ├── 02_store_price_comparison.sql
│   └── 03_price_history_summary.sql
│
└── brand/
    ├── 01_watchlist_summary.sql
    ├── 02_brand_demand_summary.sql
    └── 03_price_competitiveness.sql
```

---

# Consumer Analytics

## 01_consumer_price_summary

Provides a summary of the latest prices available across all retailers for every tracked product.

Key metrics:

- Lowest current price
- Highest current price
- Average current price
- Number of stores currently selling the product

---

## 02_store_price_comparison

Provides a store-wise comparison of the latest prices.

This view powers:

- Store comparison tables
- Lowest price identification
- Retailer comparison visuals

---

## 03_price_history_summary

Provides historical price observations for every product and store.

This view powers:

- Price trend analysis
- Historical price charts
- Time-series reporting

---

# Brand Analytics

## 01_watchlist_summary

Summarizes customer demand at the product level.

Key metrics:

- Total watchlists
- Active watchlists
- Average target price
- Current average market price
- Price gap

---

## 02_brand_demand_summary

Aggregates demand metrics at the brand level.

Key metrics:

- Total products tracked
- Total watchlists
- Active watchlists
- Average target price
- Average market price
- Average price gap

---

## 03_price_competitiveness

Measures pricing competitiveness across retailers.

Key metrics:

- Cheapest retailer
- Cheapest price
- Highest price
- Price difference
- Percentage price difference
- Number of retailers selling

---

# Dashboard Usage

These views are designed to power two reporting dashboards.

## Consumer Dashboard

- Current price overview
- Price history
- Store comparison
- Lowest available price

## Brand Intelligence Dashboard

- Product demand
- Customer willingness to pay
- Pricing competitiveness
- Brand-level demand analytics

---

# Design Principles

The Analytics Layer follows the following principles:

- Reporting-friendly SQL views
- Separation from transactional tables
- Reusable semantic layer
- Power BI optimized
- Modular design