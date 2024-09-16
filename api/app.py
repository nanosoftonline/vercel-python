from flask import Flask, request, jsonify
from pymongo import MongoClient
import certifi
app = Flask(__name__)


mongodb_uri = "mongodb+srv://smithjshaw:AtlasPassword2024@capetown.atlxp9f.mongodb.net/?retryWrites=true&w=majority&appName=CapeTown"
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
db = client.get_database("DB1")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/hello")
def hello():
    return "<h2>Hello Again!</h2>"

@app.route("/prod/<int:num1>/<int:num2>")
def prod(num1, num2):
    return f"<h2>The product of {num1} and {num2} is {num1 * num2}</h2>"

@app.route("/add/<int:num1>/<int:num2>")
def add(num1, num2):
    return f"<h2>The sum of {num1} and {num2} is {num1 + num2}</h2>"

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        user = request.json
        result = db.get_collection("users").insert_one(user)
        return jsonify({"id": str(result.inserted_id)}), 201
    else:
        users = list(db.get_collection("users").find({}, {"_id": 0}))

        return jsonify(users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)

