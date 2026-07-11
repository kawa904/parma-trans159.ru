import aiosqlite
from datetime import datetime

DB_PATH = "orders.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                message TEXT NOT NULL,
                consent BOOLEAN NOT NULL,
                consent_ads BOOLEAN DEFAULT 0,
                ip TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def save_order(order_data: dict):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO orders (name, phone, message, consent, consent_ads, ip, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data['name'],
            order_data['phone'],
            order_data['message'],
            order_data['consent'],
            order_data['consent_ads'],
            order_data['ip'],
            order_data['user_agent']
        ))
        await db.commit()