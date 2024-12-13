import os
from flask import Flask
from pymongo import MongoClient
import certifi
from routes.home import router as home_router    
from routes.users import router as users_router

app = Flask(__name__)

mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
app.db = client.get_database("DB1")


app.register_blueprint(users_router)
app.register_blueprint(home_router)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5555)
