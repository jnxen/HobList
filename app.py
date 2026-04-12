from flask import Flask, render_template, request, redirect
import sqlite3
import uuid
from rss import save_rss
from db import db_for_feed

app = Flask(__name__)

db_for_feed()


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id TEXT PRIMARY KEY,
        name TEXT,
        brand TEXT,
        ETA TEXT,
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


@app.route("/")
def landing():
    return render_template("index.html")

# Add item


@app.route("/add_items")
def add_items():
    return render_template("add_to_cart.html")


@app.route("/feed")
def feed():
    save_rss()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, link, source, date
    FROM feed
    ORDER BY date DESC
""")

    items = cursor.fetchall()
    conn.close()

    return render_template("feed.html", items=items)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    brand = request.form["brand"]
    ETA = request.form["ETA"]
    price = float(request.form["price"])
    quantity = int(request.form["quantity"])

    amount = price * quantity

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO items (item_id, name, brand, ETA, price, quantity, amount)
    VALUES (?, ?, ?, ? , ?, ?, ?)
""", (str(uuid.uuid4()),
      name,
      brand,
      ETA,
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
    return render_template("list.html")


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

    ETA = request.form["ETA"]
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
    elif quantity_input == 0:
        new_quantity = current_quantity
    else:
        new_quantity = current_quantity - abs(quantity_input)

    new_amount = price * new_quantity

    # Update DB
    cursor.execute("""
        UPDATE items
        SET 
            ETA = ?,
            price = ?,
            quantity = ?,
            amount = ?
        WHERE item_id = ?
    """, (ETA, price, new_quantity, new_amount, item_id))

    conn.commit()
    conn.close()

    return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True)
