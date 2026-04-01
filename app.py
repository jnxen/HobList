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
@app.route("/")
def index():
    return render_template("index.html")

# Add item
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    brand = request.form["brand"]
    amount = float(request.form["amount"])
    quantity = int(request.form["quantity"])

    data = load_data()
    data.append({"item_id":str(uuid.uuid4()), "name": name, "amount": amount, "brand" : brand, "quantity": quantity})
    save_data(data)

    return redirect("/list")

#delete function
@app.route("/delete/<item_id>", methods = ["POST"])
def delete_item(item_id):
    data = load_data()
    data = [item for item in data if item["item_id"] != item_id]
    save_data(data)
    return redirect("/list")

# Show list
@app.route("/list")
def list_items():
    data = load_data()
    total = sum(item["amount"] for item in data)

    return render_template("list.html", items=data, total=total)

if __name__ == "__main__":
    app.run(debug=True)