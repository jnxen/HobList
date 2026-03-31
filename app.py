from flask import Flask, render_template, request, redirect
import json

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
    amount = float(request.form["amount"])

    data = load_data()
    data.append({"name": name, "amount": amount})
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