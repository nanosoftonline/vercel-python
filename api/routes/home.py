from flask import Blueprint, render_template
router = Blueprint('home', __name__, url_prefix="/")

@router.route("/")
def hello_world():
    return render_template("index.html")