from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['upass']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """)

        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/vegmenu")
def vegmenu():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM foods WHERE food_type='Veg'"
    )

    foods = cursor.fetchall()

    conn.close()

    return render_template(
        "vegmenu.html",
        foods=foods
    )


@app.route("/nonvegmenu")
def nonvegmenu():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM foods WHERE food_type='Non Veg'"
    )

    foods = cursor.fetchall()

    conn.close()

    return render_template(
        "nonvegmenu.html",
        foods=foods
    )

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM foods")
    foods = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        foods=foods
    )


# ---------------- MENU ----------------

@app.route("/menu")
def menu():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "menu.html",
        categories=categories
    )

# ---------------- ADD CATEGORY ----------------

@app.route("/add_category", methods=["GET", "POST"])
def add_category():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT,
        image TEXT
    )
    """)

    if request.method == "POST":

        category = request.form["category"]

        image = request.files["category_image"]

        filename = secure_filename(image.filename)

        # Save image inside static folder
        image.save(os.path.join("static", filename))

        # Save image filename in database
        cursor.execute("""
            INSERT INTO categories(category_name, image)
            VALUES(?, ?)
        """, (category, filename))

        conn.commit()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    conn.close()

    return render_template(
        "add_category.html",
        categories=categories
    )

@app.route("/foods/<int:category_id>")
def foods(category_id):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            foods.id,
            foods.food_name,
            foods.category_id,
            foods.price,
            foods.discount,
            foods.description,
            foods.image,
            categories.image AS category_image
        FROM foods
        JOIN categories
        ON foods.category_id = categories.id
        WHERE foods.category_id = ?
    """, (category_id,))

    foods = cursor.fetchall()

    conn.close()

    return render_template(
        "foods.html",
        foods=foods
    )
@app.route("/manage_food", methods=["GET", "POST"])
def manage_food():

    conn = sqlite3.connect("users.db")   # ✅ Correct
    cursor = conn.cursor()

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

    if request.method == "POST":

        food = request.form["food"]
        price = request.form["price"]
        category_id = request.form["category_id"]
        food_type = request.form["food_type"]
        discount = request.form["discount"]
        description = request.form["description"]

        image = request.files["food_image"]

        filename = secure_filename(image.filename)

        image.save(
            os.path.join("static", filename)
        )

        cursor.execute("""
        INSERT INTO foods(
            food_name,
            category_id,
            food_type,
            price,
            discount,
            description,
            image
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            food,
            category_id,
            food_type,
            price,
            discount,
            description,
            filename
        ))

        conn.commit()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    cursor.execute("SELECT * FROM foods")
    foods = cursor.fetchall()

    conn.close()

    return render_template(
        "manage_food.html",
        categories=categories,
        foods=foods
    )

@app.route("/feedback")
def feedback():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT
    )
    """)

    cursor.execute("SELECT * FROM feedback")

    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        "feedback.html",
        feedbacks=feedbacks
    )

@app.route("/delete_food/<int:id>")
def delete_food(id):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM foods WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("manage_food"))


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Simple admin login
        if username == "admin" and password == "12345":
            return redirect(url_for("dashboard"))

        return "Invalid Admin Login"

    return render_template("admin.html")


@app.route("/category/<int:id>")
def category_food(id):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM foods
    WHERE category_id = ?
    """, (id,))

    foods = cursor.fetchall()

    conn.close()

    return render_template(
        "category_foods.html",
        foods=foods
    )

@app.route('/order')
def order():

    id = request.args.get('id')

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM foods WHERE id=?",
        (id,)
    )

    food = cursor.fetchone()

    conn.close()

    if food is None:
        return "Food not found"

    return render_template("order.html", food=food)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/confirm')
def confirm():
    return render_template("confirm.html")


@app.route('/payment')
def payment():

    amount = request.args.get('amount')

    return render_template(
        "payment.html",
        amount=amount
    )


if __name__ == '__main__':
    app.run(debug=True)