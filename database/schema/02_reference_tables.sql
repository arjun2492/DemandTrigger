/*
==========================================================
IntentIQ - Purchase Intent Intelligence Platform

File: 02_reference_tables.sql
Description: Creates all reference tables.

Author: Arjun S Nair
==========================================================
*/

USE intentiq;

-- ======================================================
-- Table: brands
-- ======================================================

CREATE TABLE IF NOT EXISTS brands(
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- ======================================================
-- Table: categories
-- ======================================================

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)ENGINE = InnoDB;

-- ======================================================
-- Table: stores
-- ======================================================

CREATE TABLE IF NOT EXISTS stores (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL UNIQUE,
    store_type VARCHAR(50) NOT NULL,
    website VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 
)ENGINE = InnoDB;

-- ======================================================
-- Table: products
-- ======================================================

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT NOT NULL,
    category_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    model_number VARCHAR(100),
    image_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL CURRENT_TIMESTAMP,

    CONSTRAINT fk_products_brand_id
    FOREIGN KEY(brand_id)
    REFERENCES brands(brand_id),

    CONSTRAINT fk_products_category_id
    FOREIGN KEY(category_id)
    REFERENCES categories(category_id)

)ENGINE = InnoDB;

-- ======================================================
-- Table: product listings
-- ======================================================

CREATE TABLE IF NOT EXISTS product_listings (
    listing_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    retailer_product_name VARCHAR(255) NOT NULL, 
    product_url VARCHAR(1000) NOT NULL,
    listing_status VARCHAR(20) DEFAULT 'Active',
    last_checked_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_listings_product_id
    FOREIGN KEY (product_id)
    REFERENCES products(product_id),

    CONSTRAINT fk_product_listings_store_id
    FOREIGN KEY (store_id),
    REFERENCES stores(store_id),

    CONSTRAINT uq_product_store
    UNIQUE (product_id, store_id)

)ENGINE = InnoDB;