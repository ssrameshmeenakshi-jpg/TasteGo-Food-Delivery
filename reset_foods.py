import sqlite3

conn = sqlite3.connect("food.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS foods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT,
    category_id INTEGER,
    price INTEGER,
    quantity INTEGER,
    restaurant TEXT,
    description TEXT,
    image TEXT
)
""")

# Insert sample foods
cursor.execute("""
INSERT INTO foods
(food_name, category_id, price, quantity, restaurant, description, image)
VALUES
('Veg Salad', 1, 120, 10, 'Saffron', 'Fresh vegetable salad', 'vegsalad.jpeg')
""")

cursor.execute("""
INSERT INTO foods
(food_name, category_id, price, quantity, restaurant, description, image)
VALUES
('Chicken Biryani', 2, 250, 20, 'Saffron', 'Spicy chicken biryani', 'biryani.jpg')
""")

conn.commit()
conn.close()

print("Foods added successfully")