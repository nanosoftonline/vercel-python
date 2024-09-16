import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
from bson import ObjectId
import certifi

app = Flask(__name__)

# MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
db = client.get_database("DB1")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/users", methods=["GET"])
def get_users():
        users = list(db.get_collection("users").find({}))
        for u in users:
           u["_id"] = str(u["_id"])     
        return jsonify(users)
    
@app.route("/users", methods=["POST"])
def insert_user():
        user = request.json
        result = db.get_collection("users").insert_one(user)
        return jsonify({"id": str(result.inserted_id)}), 201
    

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
        result = db.get_collection("users").delete_one({"_id": ObjectId(id)})
        return jsonify({"deleted_count": result.deleted_count}), 200
    

@app.route("/users/<id>", methods=["GET"])
def get_user(id):
        result = db.get_collection("users").find_one({"_id": ObjectId(id)})
        result["_id"] = str(result["_id"])
        return jsonify(result), 200

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
        user = request.json
        result = db.get_collection("users").update_one({"_id": ObjectId(id)}, {"$set": user})
        return jsonify({"modified_count": result.modified_count}), 200
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5555)