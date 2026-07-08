"""
==========================================================
IntentIQ

File: generate_demo_data.py

Description:
Generates realistic demo data for IntentIQ.

Author: Arjun S Nair
==========================================================
"""

from src.data_generation.demo_data_generator import (
    cleanup_demo_data,
    generate_demo_users,
    insert_demo_users,
    generate_demo_watchlists,
    insert_demo_watchlists,
    generate_target_price_history,
    insert_target_price_history
)

from src.config.logger import logger


def main():

    logger.info(
        "Starting demo data generation..."
    )

    cleanup_demo_data()

    users = generate_demo_users()
    insert_demo_users(users)

    watchlists = generate_demo_watchlists()
    insert_demo_watchlists(watchlists)

    history = generate_target_price_history()
    insert_target_price_history(history)

    logger.info("====================================")
    logger.info("Demo Data Generation Summary")
    logger.info(f"Users Generated: {len(users)}")
    logger.info(f"Watchlists Generated: {len(watchlists)}")
    logger.info(f"Target History Records: {len(history)}")
    logger.info("Demo data generation completed.")
    logger.info("====================================")


if __name__ == "__main__":
    main()