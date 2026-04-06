from flask import Flask, render_template, request, redirect
import json
import uuid

app = Flask(__name__)

# Load data


def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return []

# Save data


def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


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

    data = load_data()
    data.append({"item_id": str(uuid.uuid4()), "name": name,
                 "brand": brand, "price": price, "quantity": quantity, "amount": amount})
    save_data(data)

    return redirect("/list")

# delete function


@app.route("/delete/<item_id>", methods=["POST"])
def delete_item(item_id):
    data = load_data()
    data = [item for item in data if item["item_id"] != item_id]
    save_data(data)
    return redirect("/list")


@app.route("/clear", methods=["POST"])
def clear_data():
    save_data([])
    return redirect("/list")
# Show list


@app.route("/list")
def list_items():
    data = load_data()
    total = sum(item["amount"] for item in data)

    return render_template("list.html", items=data, total=total)


@app.route("/edit/<item_id>")
def edit_item(item_id):
    data = load_data()
    item_to_edit = None
    for item in data:
        if item["item_id"] == item_id:
            item_to_edit = item
            break
    return render_template("edit.html", item=item_to_edit)


@app.route("/update/<item_id>", methods=["POST"])
def update_item(item_id):
    data = load_data()
    for item in data:
        if item['item_id'] == item_id:
            item['name'] = request.form['name']
            item['brand'] = request.form['brand']
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])
            item['price'] = price
            if quantity > 0:
                item['quantity'] += quantity
                item['amount'] = price * item['quantity']
            else:
                item['quantity'] -= abs(quantity)
                item['amount'] = price * item["quantity"]

            break

    save_data(data)
    return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True)
