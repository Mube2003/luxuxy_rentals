import os
import sqlite3
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "luxury_rentals.db")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")
MESSAGES_FILE = os.path.join(BASE_DIR, "contact_messages.json")
REVIEWS_FILE = os.path.join(BASE_DIR, "reviews.json")
WISHLIST_FILE = os.path.join(BASE_DIR, "wishlist.json")
LOYALTY_FILE = os.path.join(BASE_DIR, "loyalty_points.json")
PROMO_FILE = os.path.join(BASE_DIR, "promo_codes.json")

SQL_CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        joined TEXT,
        role TEXT DEFAULT 'customer'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        address TEXT,
        item_id INTEGER,
        item_name TEXT,
        item_emoji TEXT,
        item_category TEXT,
        price REAL,
        quantity INTEGER,
        deposit REAL,
        subtotal REAL,
        delivery_fee REAL,
        total REAL,
        pay_method TEXT,
        event_date TEXT,
        status TEXT,
        placed_at TEXT,
        placed_ip TEXT,
        items_json TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        email TEXT,
        phone TEXT,
        message TEXT,
        sent_at TEXT,
        admin_reply TEXT,
        reply_subject TEXT,
        reply_sent_at TEXT,
        reply_to TEXT,
        status TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        username TEXT,
        name TEXT,
        rating INTEGER,
        comment TEXT,
        created_at TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS wishlist_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        item_id INTEGER,
        item_name TEXT,
        emoji TEXT,
        price REAL,
        quantity INTEGER,
        item_json TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS loyalty (
        username TEXT PRIMARY KEY,
        points INTEGER,
        referral_code TEXT,
        referred_friends INTEGER,
        FOREIGN KEY(username) REFERENCES users(username)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS promo_codes (
        code TEXT PRIMARY KEY,
        discount REAL,
        type TEXT,
        active INTEGER
    );
    """,
]


def get_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn):
    cursor = conn.cursor()
    for sql in SQL_CREATE_TABLES:
        cursor.execute(sql)
    conn.commit()


def load_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def migrate_users(conn):
    users = load_json(USERS_FILE, {})
    cursor = conn.cursor()
    for username, data in users.items():
        cursor.execute(
            "INSERT OR REPLACE INTO users (username, password, full_name, email, phone, city, joined, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                username,
                data.get("password", ""),
                data.get("full_name", ""),
                data.get("email", ""),
                data.get("phone", ""),
                data.get("city", ""),
                data.get("joined", ""),
                data.get("role", "customer"),
            ),
        )
    conn.commit()


def migrate_orders(conn):
    orders = load_json(ORDERS_FILE, {})
    cursor = conn.cursor()
    for order_id, order in orders.items():
        cursor.execute(
            "INSERT OR REPLACE INTO orders (order_id, username, full_name, email, phone, city, address, item_id, item_name, item_emoji, item_category, price, quantity, deposit, subtotal, delivery_fee, total, pay_method, event_date, status, placed_at, placed_ip, items_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                order_id,
                order.get("username"),
                order.get("full_name"),
                order.get("email"),
                order.get("phone"),
                order.get("city"),
                order.get("address"),
                order.get("item_id"),
                order.get("item_name"),
                order.get("item_emoji"),
                order.get("item_category"),
                order.get("price"),
                order.get("quantity"),
                order.get("deposit"),
                order.get("subtotal"),
                order.get("delivery_fee"),
                order.get("total"),
                order.get("pay_method"),
                order.get("event_date"),
                order.get("status"),
                order.get("placed_at"),
                order.get("placed_ip"),
                json.dumps(order.get("items")) if order.get("items") is not None else None,
            ),
        )
    conn.commit()


def migrate_messages(conn):
    messages = load_json(MESSAGES_FILE, [])
    cursor = conn.cursor()
    for message in messages:
        cursor.execute(
            "INSERT INTO messages (username, name, email, phone, message, sent_at, admin_reply, reply_subject, reply_sent_at, reply_to, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                message.get("username"),
                message.get("name"),
                message.get("email"),
                message.get("phone"),
                message.get("message"),
                message.get("sent_at"),
                message.get("admin_reply"),
                message.get("reply_subject"),
                message.get("reply_sent_at"),
                message.get("reply_to"),
                message.get("status"),
            ),
        )
    conn.commit()


def migrate_reviews(conn):
    reviews = load_json(REVIEWS_FILE, {})
    cursor = conn.cursor()
    for item_id, review_list in reviews.items():
        for review in review_list:
            cursor.execute(
                "INSERT INTO reviews (item_id, username, name, rating, comment, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    item_id,
                    review.get("username"),
                    review.get("name"),
                    review.get("rating"),
                    review.get("comment"),
                    review.get("created_at", ""),
                ),
            )
    conn.commit()


def migrate_wishlist(conn):
    wishlist = load_json(WISHLIST_FILE, {})
    cursor = conn.cursor()
    for username, items in wishlist.items():
        for item in items:
            cursor.execute(
                "INSERT INTO wishlist_items (username, item_id, item_name, emoji, price, quantity, item_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    username,
                    item.get("id"),
                    item.get("name"),
                    item.get("emoji"),
                    item.get("price"),
                    item.get("quantity", 1),
                    json.dumps(item),
                ),
            )
    conn.commit()


def migrate_loyalty(conn):
    loyalty = load_json(LOYALTY_FILE, {})
    cursor = conn.cursor()
    for username, data in loyalty.items():
        cursor.execute(
            "INSERT OR REPLACE INTO loyalty (username, points, referral_code, referred_friends) VALUES (?, ?, ?, ?)",
            (
                username,
                data.get("points", 0),
                data.get("referral_code"),
                data.get("referred_friends", 0),
            ),
        )
    conn.commit()


def migrate_promo_codes(conn):
    promos = load_json(PROMO_FILE, {})
    cursor = conn.cursor()
    for code, data in promos.items():
        cursor.execute(
            "INSERT OR REPLACE INTO promo_codes (code, discount, type, active) VALUES (?, ?, ?, ?)",
            (
                code,
                data.get("discount", 0),
                data.get("type", "fixed"),
                1 if data.get("active", True) else 0,
            ),
        )
    conn.commit()


def initialize_database():
    print(f"Creating SQLite database at: {DATABASE_FILE}")
    conn = get_connection()
    create_tables(conn)
    migrate_users(conn)
    migrate_orders(conn)
    migrate_messages(conn)
    migrate_reviews(conn)
    migrate_wishlist(conn)
    migrate_loyalty(conn)
    migrate_promo_codes(conn)
    conn.close()
    print("Database initialization complete.")


if __name__ == "__main__":
    initialize_database()
