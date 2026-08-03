import aiosqlite

from config import DB_NAME


async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:

        # Користувачі
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT
        )
        """)

        # Категорії
        await db.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
        """)

        # Товари
        await db.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT,
            description TEXT,
            price REAL,
            photo TEXT,
            content TEXT
        )
        """)

        # Склад товарів
        await db.execute("""
        CREATE TABLE IF NOT EXISTS stock(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            content TEXT,
            is_used INTEGER DEFAULT 0
        )
        """)

        # Замовлення
        await db.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            invoice_id INTEGER,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()


async def add_product(category, name, description, price, photo, content):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO products
            (category_id, name, description, price, photo, content)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                category,
                name,
                description,
                price,
                photo,
                content
            )
        )
        await db.commit()


async def get_products(category):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT
                id,
                name,
                description,
                price,
                photo
            FROM products
            WHERE category_id = ?
            """,
            (category,)
        )
        return await cursor.fetchall()


async def get_product(product_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT
                id,
                name,
                description,
                price,
                photo,
                content
            FROM products
            WHERE id = ?
            """,
            (product_id,)
        )
        return await cursor.fetchone()


async def create_order(user_id, product_id, invoice_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            INSERT INTO orders
            (user_id, product_id, invoice_id)
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                product_id,
                invoice_id
            )
        )
        await db.commit()
        return cursor.lastrowid


async def get_order_invoice(order_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT invoice_id
            FROM orders
            WHERE id = ?
            """,
            (order_id,)
        )
        return await cursor.fetchone()


async def update_order_status(order_id, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE orders
            SET status = ?
            WHERE id = ?
            """,
            (
                status,
                order_id
            )
        )
        await db.commit()


async def get_pending_orders():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT
                id,
                user_id,
                product_id,
                invoice_id
            FROM orders
            WHERE status = 'pending'
            """
        )
        return await cursor.fetchall()


async def add_stock(product_id, content):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO stock(product_id, content)
            VALUES (?, ?)
            """,
            (product_id, content)
        )
        await db.commit()


async def get_free_stock(product_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT id, content
            FROM stock
            WHERE product_id = ?
            AND is_used = 0
            LIMIT 1
            """,
            (product_id,)
        )
        return await cursor.fetchone()


async def use_stock(stock_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE stock
            SET is_used = 1
            WHERE id = ?
            """,
            (stock_id,)
        )
        await db.commit()

async def use_stock(stock_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE stock
            SET is_used = 1
            WHERE id = ?
            """,
            (stock_id,)
        )
        await db.commit()


async def get_all_products():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT id, name
            FROM products
            ORDER BY id
            """
        )
        return await cursor.fetchall()   

async def get_user_orders(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT
                products.name,
                products.price,
                orders.status,
                orders.created_at
            FROM orders
            JOIN products
            ON products.id = orders.product_id
            WHERE orders.user_id = ?
            ORDER BY orders.id DESC
            """,
            (user_id,)
        )
        return await cursor.fetchall()    

async def get_statistics():
    async with aiosqlite.connect(DB_NAME) as db:

        users = await db.execute(
            "SELECT COUNT(*) FROM users"
        )
        users = (await users.fetchone())[0]

        products = await db.execute(
            "SELECT COUNT(*) FROM products"
        )
        products = (await products.fetchone())[0]

        orders = await db.execute(
            "SELECT COUNT(*) FROM orders"
        )
        orders = (await orders.fetchone())[0]

        paid = await db.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE status='paid'
            """
        )
        paid = (await paid.fetchone())[0]

        money = await db.execute(
            """
            SELECT IFNULL(SUM(products.price),0)
            FROM orders
            JOIN products
            ON orders.product_id = products.id
            WHERE orders.status='paid'
            """
        )
        money = (await money.fetchone())[0]

        return users, products, orders, paid, money     