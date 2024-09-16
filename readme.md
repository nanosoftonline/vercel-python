# Python Web App hosted on Vercel
In repository we'll show how to create a python web application and connect to a MongoDB database

Flask is a micro web framework that is used to build web applications. If you're comming from node, it is very much like the express web framework. You can build an application with a single file

## 1. Create a virtual environment
The virtual environment allows you to create and maintain an isolated project where you can install the packages that are relavent to this project. Within this environment we can then create a requirements.txt which will help when we deploy the project to production.
```bash
python3 -m venv .venv
```
This creates the envorinment and puts it in a hidden directory. We then need to activate the env

```bash
source .venv/bin/activate
```

To check if you're in the local environment run the following command:

```bash
pip3 freeze
```
You'll notice that there are currently no packages installed. If you run this command from another uninitialised environment you'll see the globally installed packages

## 2. Install Flask
Once you have the virtual environment activated you have to install flask
```bash
pip3 install flask
```
I can run "pip3 freeze" to show all the installed in this env

## 3. Create a file for your web application
```py
#app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) # Dev only- run in debug to restart the server on code

```

debug=True: while developing you need this param, You don't want to run this in production

we need to create a requirements.txt to log all the packages installed

```bash
pip3 freeze > requirements.txt
```

## 4. Run the application
To run the application simply run
```
python3 app.py
```

## 5. MongoDB integration

To connect this project to a MongoDB Atlas instance, first install the PyMongo library by running 

```bash 
pip3 install pymongo certifi
``` 
Then, create a MongoDB Atlas account and set up a cluster if you haven't already. Obtain your connection string from the Atlas dashboard. 

In your `app.py` file, import PyMongo and establish a connection to your database using the connection string. 

```py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
mongodb_uri = "mongodb+srv://..."
client = MongoClient(mongodb_uri)
db = client["DB1]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        user = request.json
        result = db.users.insert_one(user)
        return jsonify({"id": str(result.inserted_id)}), 201
    else:
        users = list(db.users.find({}))
        return jsonify(users)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
```

Update the requirements

```bash
pip3 freeze > requirements.txt
```

And run the project again to test the db connection


