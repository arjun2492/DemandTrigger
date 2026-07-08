from src.data_generation.demo_data_generator import *

cleanup_demo_data()

users = generate_demo_users()

insert_demo_users(users)

watchlists = generate_demo_watchlists()

insert_demo_watchlists(watchlists)

print(len(watchlists))