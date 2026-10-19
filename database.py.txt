
import sqlite3

DB_NAME = "stylemind.db"


def connect_db():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT NOT NULL DEFAULT 'Tetouan',
                address TEXT DEFAULT '',
                phone TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shop_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT DEFAULT '',
                price REAL NOT NULL,
                color TEXT DEFAULT '',
                sizes TEXT DEFAULT '',
                style TEXT DEFAULT '',
                image_url TEXT DEFAULT '',
                in_stock INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (shop_id) REFERENCES shops(id)
            )
        """)


def add_shop(name, city="Tetouan", address="", phone=""):
    with connect_db() as conn:
        cursor = conn.execute(
            """INSERT INTO shops (name, city, address, phone)
               VALUES (?, ?, ?, ?)""",
            (name, city, address, phone)
        )
        return cursor.lastrowid


def add_product(
    shop_id, name, category, price,
    description="", color="", sizes="",
    style="", image_url="", in_stock=True
):
    with connect_db() as conn:
        cursor = conn.execute(
            """INSERT INTO products
               (shop_id, name, category, price, description,
                color, sizes, style, image_url, in_stock)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                shop_id, name, category, price, description,
                color, sizes, style, image_url, int(in_stock)
            )
        )
        return cursor.lastrowid


def get_shops():
    with connect_db() as conn:
        return conn.execute(
            "SELECT * FROM shops ORDER BY name"
        ).fetchall()


def get_products():
    with connect_db() as conn:
        return conn.execute("""
            SELECT products.*, shops.name AS shop_name,
                   shops.address AS shop_address,
                   shops.phone AS shop_phone
            FROM products
            JOIN shops ON shops.id = products.shop_id
            WHERE products.in_stock = 1
            ORDER BY products.created_at DESC
        """).fetchall()


if __name__ == "__main__":
    init_db()
    print("StyleMind AI database created successfully!")
