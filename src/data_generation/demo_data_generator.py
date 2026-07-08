"""
==========================================================
IntentIQ

File: demo_data_generator.py

Description:
Helper functions for generating realistic
demo data for IntentIQ.

Author: Arjun S Nair
==========================================================
"""

import random
from datetime import datetime, timedelta

from src.database.connection import get_connection
from src.config.logger import logger


# ==========================================================
# Configuration
# ==========================================================

NUMBER_OF_USERS = 50

STATES = [
    "Kerala",
    "Karnataka",
    "Tamil Nadu",
    "Maharashtra",
    "Delhi",
    "Telangana",
    "Gujarat",
    "West Bengal",
    "Rajasthan",
    "Uttar Pradesh"
]


# ==========================================================
# Fetch Products
# ==========================================================

def fetch_products_with_prices():
    """
    Fetches all products along with the
    lowest currently available price.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT

            p.product_id,

            p.product_name,

            b.brand_name,

            MIN(lp.price) AS current_price

        FROM products p

        JOIN brands b
            ON p.brand_id = b.brand_id

        JOIN latest_prices lp
            ON p.product_id = lp.product_id

        GROUP BY

            p.product_id,

            p.product_name,

            b.brand_name

        ORDER BY

            b.brand_name,

            p.product_name;
    """

    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


# ==========================================================
# Cleanup Existing Demo Data
# ==========================================================

def cleanup_demo_data():
    """
    Deletes previously generated demo data.

    Order:
    1. target_price_history
    2. watchlists
    3. users
    """

    connection = get_connection()
    cursor = connection.cursor()

    logger.info("Cleaning previous demo data...")

    cursor.execute("""
        DELETE tph
        FROM target_price_history tph
        JOIN watchlists w
            ON tph.watchlist_id = w.watchlist_id
        JOIN users u
            ON w.user_id = u.user_id
        WHERE u.email LIKE 'demo_user%';
    """)

    cursor.execute("""
        DELETE w
        FROM watchlists w
        JOIN users u
            ON w.user_id = u.user_id
        WHERE u.email LIKE 'demo_user%';
    """)

    cursor.execute("""
        DELETE
        FROM users
        WHERE email LIKE 'demo_user%';
    """)

    connection.commit()

    cursor.close()
    connection.close()

    logger.info("Previous demo data removed.")


# ==========================================================
# Generate Demo Users
# ==========================================================

def generate_demo_users():
    """
    Generates demo users.
    """

    users = []

    today = datetime.now()

    for i in range(1, NUMBER_OF_USERS + 1):

        created_at = today - timedelta(
            days=random.randint(1, 365)
        )

        users.append(

            (
                f"demo_user{i:03}@example.com",

                f"9{random.randint(100000000, 999999999)}",

                random.choice(STATES),

                created_at
            )

        )

    return users


# ==========================================================
# Insert Demo Users
# ==========================================================

def insert_demo_users(users):
    """
    Inserts demo users into database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO users
        (
            email,
            whatsapp_number,
            state,
            created_at
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        );
    """

    cursor.executemany(query, users)

    connection.commit()

    logger.info(
        f"Inserted {cursor.rowcount} demo users."
    )

    cursor.close()
    connection.close()


# ==========================================================
# Fetch Demo Users
# ==========================================================

def fetch_demo_users():
    """
    Fetches generated demo users.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            user_id,
            created_at
        FROM users
        WHERE email LIKE 'demo_user%';
    """)

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users

# ==========================================================
# Product Weights
# ==========================================================

def assign_product_weights(products):
    """
    Assigns popularity weights to products.
    Higher weight = more likely to be watchlisted.
    """

    weighted_products = []

    for product in products:

        name = product["product_name"].lower()

        weight = 3

        if "iphone" in name:
            weight = 10

        elif "airpods" in name:
            weight = 10

        elif "wh-1000xm5" in name:
            weight = 9

        elif "qc ultra" in name:
            weight = 8

        elif "galaxy" in name:
            weight = 8

        elif "ipad" in name:
            weight = 7

        elif "macbook" in name:
            weight = 7

        elif "sony" in name:
            weight = 6

        elif "bose" in name:
            weight = 6

        elif "jbl" in name:
            weight = 5

        product["weight"] = weight

        weighted_products.append(product)

    return weighted_products


# ==========================================================
# Generate Demo Watchlists
# ==========================================================

def generate_demo_watchlists():

    """
    Generates realistic watchlists
    for demo users.
    """

    users = fetch_demo_users()

    products = assign_product_weights(
        fetch_products_with_prices()
    )

    watchlists = []

    for user in users:

        watchlist_count = random.randint(2, 6)

        chosen_products = []

        while len(chosen_products) < watchlist_count:

            product = random.choices(
                products,
                weights=[
                    p["weight"]
                    for p in products
                ],
                k=1
            )[0]

            if product["product_id"] not in chosen_products:

                chosen_products.append(
                    product["product_id"]
                )

                current_price = float(
                    product["current_price"]
                )

                discount = random.uniform(
                    0.75,
                    0.98
                )

                target_price = round(
                    current_price * discount,
                    2
                )

                watchlists.append(

                    (
                        user["user_id"],

                        product["product_id"],

                        target_price,

                        random.random() < 0.9,

                        user["created_at"]
                    )

                )

    return watchlists


# ==========================================================
# Insert Demo Watchlists
# ==========================================================

def insert_demo_watchlists(watchlists):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO watchlists
        (
            user_id,
            product_id,
            current_target_price,
            is_active,
            created_at
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        );
    """

    cursor.executemany(
        query,
        watchlists
    )

    connection.commit()

    logger.info(
        f"Inserted {cursor.rowcount} watchlists."
    )

    cursor.close()
    connection.close()


# ==========================================================
# Fetch Demo Watchlists
# ==========================================================

def fetch_demo_watchlists():
    """
    Fetches all watchlists belonging to demo users.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            w.watchlist_id,
            w.current_target_price,
            w.created_at
        FROM watchlists w
        JOIN users u
            ON w.user_id = u.user_id
        WHERE u.email LIKE 'demo_user%';
    """

    cursor.execute(query)

    watchlists = cursor.fetchall()

    cursor.close()
    connection.close()

    return watchlists


# ==========================================================
# Generate Target Price History
# ==========================================================

def generate_target_price_history():
    """
    Generates realistic target price history
    for a subset of demo watchlists.
    """

    history = []

    watchlists = fetch_demo_watchlists()

    for watchlist in watchlists:

        # Around 30% of users modify their target price
        if random.random() > 0.30:
            continue

        number_of_changes = random.randint(1, 3)

        base_price = float(
            watchlist["current_target_price"]
        )

        created_at = watchlist["created_at"]

        for _ in range(number_of_changes):

            price_change = random.uniform(
                -0.05,
                0.05
            )

            new_price = round(
                base_price * (1 + price_change),
                2
            )

            updated_at = created_at + timedelta(
                days=random.randint(5, 180)
            )

            history.append(

                (
                    watchlist["watchlist_id"],
                    new_price,
                    updated_at
                )

            )

            base_price = new_price

    return history


# ==========================================================
# Insert Target Price History
# ==========================================================

def insert_target_price_history(history):
    """
    Inserts generated target price history.
    """

    if not history:
        logger.info(
            "No target price history generated."
        )
        return

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO target_price_history
        (
            watchlist_id,
            target_price,
            updated_at
        )
        VALUES
        (
            %s,
            %s,
            %s
        );
    """

    cursor.executemany(query, history)

    connection.commit()

    logger.info(
        f"Inserted {cursor.rowcount} target price history records."
    )

    cursor.close()
    connection.close()