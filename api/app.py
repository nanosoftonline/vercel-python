import os
from flask import Flask
from pymongo import MongoClient
import certifi

app = Flask(__name__)

mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
app.db = client.get_database("DB1")

if os.getenv("ENV") == "DEV":
    from routes.users import router as users_router
    from routes.home import router as home_router    
else:
    from api.routes.users import router as users_router
    from api.routes.home import router as home_router

app.register_blueprint(users_router)
app.register_blueprint(home_router)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5555)
