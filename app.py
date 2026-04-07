from flask import Flask, render_template, request, redirect
import sqlite3
import uuid

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id TEXT PRIMARY KEY,
        name TEXT,
        brand TEXT,
        price REAL,
        quantity INTEGER,
        amount REAL
    )
    """)

    conn.commit()
    conn.close()


init_db()


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home page (form)
posts = [
    {
        "user": "Carlos M.",
        "caption": "Just picked up this 1:64 Hot Wheels Ferrari F40! The detail on the wheels is insane 🔥",
        "image": "https://via.placeholder.com/500x300",
        "likes": 24,
        "time": "2 hours ago"
    },
    {
        "user": "Ana R.",
        "caption": "My 1:18 scale Lamborghini Countach finally arrived from Japan. Worth the wait!",
        "image": "https://via.placeholder.com/500x300",
        "likes": 47,
        "time": "5 hours ago"
    },
    {
        "user": "Marco D.",
        "caption": "No image today, just sharing — found a vintage Matchbox Superfast at a flea market for $2!",
        "image": None,   # No image for this post
        "likes": 15,
        "time": "Yesterday"
    },
]


@app.route("/")
def landing():
    return render_template("index.html", posts=posts)

# Add item


@app.route("/add_items")
def add_items():
    return render_template("add_to_cart.html")


@app.route("/feed")
def feed():
    return render_template("feed.html", posts=posts)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    brand = request.form["brand"]
    price = float(request.form["price"])
    quantity = int(request.form["quantity"])

    amount = price * quantity

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO items (item_id, name, brand, price, quantity, amount)
    VALUES (?, ?, ?, ?, ?, ?)
""", (str(uuid.uuid4()),
      name,
      brand,
      price,
      quantity,
      amount
      ))
    conn.commit()
    conn.close()
    return redirect("/list")

# delete function


@app.route("/delete/<item_id>", methods=["POST"])
def delete_item(item_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))

    conn.commit()
    conn.close()


@app.route("/clear", methods=["POST"])
def clear_data():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM items")

    conn.commit()
    conn.close()
    return render_template("list.html")
# Show list


@app.route("/list")
def list_items():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()

    conn.close()

    items = [dict(row) for row in rows]
    total = sum(item["amount"] for item in items)

    return render_template("list.html", items=items, total=total)


@app.route("/edit/<item_id>")
def edit_item(item_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE item_id =  ?",
                   (item_id,)
                   )
    row = cursor.fetchone()
    conn.close()
    return render_template("edit.html", item=row)


@app.route("/update/<item_id>", methods=["POST"])
def update_item(item_id):

    name = request.form["name"]
    brand = request.form["brand"]
    quantity_input = int(request.form["quantity"])
    price = float(request.form["price"])

    conn = get_db()
    cursor = conn.cursor()

    # Get current quantity first
    cursor.execute("SELECT quantity FROM items WHERE item_id = ?", (item_id,))
    row = cursor.fetchone()

    current_quantity = row["quantity"]

    # Apply your logic
    if quantity_input > 0:
        new_quantity = current_quantity + quantity_input
    else:
        new_quantity = current_quantity - abs(quantity_input)

    new_amount = price * new_quantity

    # Update DB
    cursor.execute("""
        UPDATE items
        SET name = ?,
            brand = ?,
            price = ?,
            quantity = ?,
            amount = ?
        WHERE item_id = ?
    """, (name, brand, price, new_quantity, new_amount, item_id))

    conn.commit()
    conn.close()

    return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True)
