import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Admin table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# Categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT,
    image TEXT
)
""")

# Foods table
cursor.execute("""
CREATE TABLE IF NOT EXISTS foods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT,
    category_id INTEGER,
    food_type TEXT,
    price INTEGER,
    discount INTEGER,
    description TEXT,
    image TEXT
)
""")

# Add default admin
cursor.execute(
    "SELECT * FROM admin WHERE username=?",
    ("admin",)
)

if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO admin(username,password) VALUES(?,?)",
        ("admin", "12345")
    )

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM foods")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.commit()
conn.close()

print("Database created successfully")
