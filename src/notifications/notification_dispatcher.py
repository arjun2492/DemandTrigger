"""
==========================================================
IntentIQ

File: notification_dispatcher.py

Description:
Fetches pending notifications, simulates sending them,
and updates their status to 'Sent'.

Author: Arjun S Nair
==========================================================
"""

from src.database.connection import get_connection

def fetch_pending_notifications():
    """
    Fetches all pending notifications.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            n.notification_id,
            u.email,
            u.whatsapp_number,
            p.product_name,
            lp.price,
            w.current_target_price
        FROM
            notifications n
        JOIN watchlists w
            ON n.watchlist_id = w.watchlist_id
        
        JOIN users u
            ON w.user_id = u.user_id

        JOIN products p
            ON w.product_id = p.product_id

        JOIN latest_prices lp
            ON n.price_id = lp.price_id

        WHERE 
            n.notification_status = 'Pending'; 
    """
    cursor.execute(query)

    notifications = cursor.fetchall()

    cursor.close()
    connection.close()

    return notifications

# ==========================
# Update Functions
# ==========================

def mark_notification_sent(notification_id):
    """
    Marks a notification as sent.
    """
    connection =  get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE notifications
        SET 
            notification_status = 'Sent',
            sent_at = NOW()
        WHERE
            notification_id = %s;
    """
    cursor.execute(query, (notification_id,))
    
    connection.commit()
    
    cursor.close()
    connection.close()

# ==========================
# Dispatcher
# ==========================

def dispatch_notifications():
    """
    Simulates sending pending notifications.
    """
    notifications = fetch_pending_notifications()

    if not notifications:
        print("No pending notifications.")
        return
    
    for notification in notifications:
        
        print("\n" + "=" * 60)

        print(f"To: {notification['email']}")

        print(f"Whatsapp: {notification['whatsapp_number']}")

        print()

        print("Price Alert!")

        print(f"Product: {notification['product_name']}")

        print(f"Current Price: ₹{notification['price']}")

        print(f"Your Target Price:₹{notification['current_target_price']}")

        print("Your target price has been reached!")

        print('='* 60)

        # Simulate successful delivery
        mark_notification_sent(
            notification["notification_id"]
        )

# ==========================
# Main
# ==========================

def main():

    dispatch_notifications()


if __name__ == "__main__":
    main()

