from flask import Blueprint, jsonify, request, current_app, render_template, redirect
from bson import ObjectId

router = Blueprint('users', __name__, url_prefix="/users")

@router.route("/", methods=["GET"])
def get_users():
    db = current_app.db
    users = list(db.get_collection("users").find({}))
    for u in users:
        u["_id"] = str(u["_id"])     
    return render_template("users.html", users=users)

@router.route("/", methods=["POST"])
def insert_user():
    db = current_app.db
    user_data = request.form.to_dict() 
    result = db.get_collection("users").insert_one(user_data)
    return redirect("/users")


@router.route("/<id>", methods=["POST"])
def form_update_user(id):
    db = current_app.db
    user = request.form.to_dict() 
    db.get_collection("users").update_one({"_id": ObjectId(id)}, {"$set": user})
    return redirect("/users", code=302)

@router.route("/<id>", methods=["DELETE"])
def delete_user(id):
    db = current_app.db
    result = db.get_collection("users").delete_one({"_id": ObjectId(id)})
    return jsonify({"deleted_count": result.deleted_count}), 200

@router.route("/<id>", methods=["GET"])
def get_user(id):

    if(id == "new"):
        return render_template("user_new.html",)
    
    db = current_app.db
    result = db.get_collection("users").find_one({"_id": ObjectId(id)})
    result["_id"] = str(result["_id"])
    
    return render_template("user_detail.html", user=result)
    # return jsonify(result), 200

@router.route("/<id>", methods=["PUT"])
def update_user(id):
    db = current_app.db
    user = request.json
    result = db.get_collection("users").update_one({"_id": ObjectId(id)}, {"$set": user})
    return jsonify({"modified_count": result.modified_count}), 200
