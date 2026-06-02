import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

# USERS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# FOOD ITEMS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    price INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    food_name TEXT NOT NULL,
    price INTEGER NOT NULL,
    status TEXT DEFAULT 'Pending'
)
''')

conn.commit()
conn.close()

print("Database and tables created successfully")