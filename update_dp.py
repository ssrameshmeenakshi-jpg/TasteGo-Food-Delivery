import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE foods
ADD COLUMN category_id INTEGER
""")

cursor.execute("""
ALTER TABLE foods
ADD COLUMN discount INTEGER
""")

cursor.execute("""
ALTER TABLE foods
ADD COLUMN description TEXT
""")

cursor.execute("""
ALTER TABLE foods
ADD COLUMN image TEXT
""")

conn.commit()
conn.close()

print("Foods table updated.")