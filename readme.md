# Python Web App hosted on Vercel

## Introduction
This guide will walk you through setting up a basic Flask web application with a virtual environment, connecting to a MongoDB Atlas instance, and running your project locally. We will start by ensuring Python 3 is installed, creating a project directory, and setting up a Python virtual environment. You'll learn how to install Flask, build a simple web app, and integrate MongoDB for data storage. Finally, we will deploy the project to Vercel for hosting, allowing you to make your application accessible online. By the end, you'll have a fully functional Flask application ready for development and deployment.

Here’s the updated section with instructions for installing Git Bash on Windows and an explanation of why it can be preferred over PowerShell:

---

##Install Python 3

If you don't already have Python 3 installed, follow the instructions for your operating system below:

### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

### On macOS using Homebrew:
```bash
brew install python3
```

### On Windows:
1. Download the latest version of Python 3 from the [official website](https://www.python.org/downloads/).
2. Run the installer and ensure the option **"Add Python to PATH"** is checked during installation.
3. Follow the prompts to complete the installation.

Additionally, it’s recommended to use **Git Bash** instead of PowerShell for running commands, especially when working with Unix-like environments (such as virtual environments or when deploying). Git Bash offers a more consistent and familiar command-line interface compared to PowerShell, aligning better with tutorials and development tools that assume a Linux-like shell.

#### Install Git Bash:
1. Download Git for Windows from the [official Git website](https://git-scm.com/download/win).
2. Run the installer, and during installation, select **"Git Bash"** as the default terminal.
3. Complete the installation.

Once installed, you can open **Git Bash** from your Start Menu or right-click in a folder and select "Git Bash Here."

#### Why use Git Bash over PowerShell:
- **Unix-like commands**: Many development guides and tools assume you're working in a Unix-like environment. Git Bash provides a terminal experience similar to macOS or Linux, making it easier to follow along with tutorials.
- **Compatibility**: Some commands used for managing virtual environments and deployments may not behave the same in PowerShell, whereas Git Bash provides a more consistent cross-platform experience.

To verify Python is installed, open Git Bash and run:

```bash
python3 --version
```

Make sure Python 3 is installed and available in your system.

--- 

## Create a Project Directory

Before setting up the virtual environment, create a directory for your project and navigate into it:

```bash
mkdir my_flask_app
cd my_flask_app
```

Now, you're ready to create the virtual environment.

---
## Create a virtual environment
The virtual environment allows you to create and maintain an isolated project where you can install the packages that are relavent to this project. Within this environment we can then create a requirements.txt which will help when we deploy the project to production.
```bash
python3 -m venv .venv
```
This creates the envorinment and puts it in a hidden directory. We then need to activate the environment

```bash
source .venv/bin/activate
```

To check if you're in the local environment run the following command:

```bash
pip3 freeze
```
You'll notice that there are currently no packages installed. If you run this command from another uninitialised environment you'll see the globally installed packages

---
##Install Flask
Once you have the virtual environment activated you have to install flask
```bash
pip3 install flask
```
I can run "pip3 freeze" to show all the installed in this environment

---
##Create a file for your web application
```py
#app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) 

```

We add the debug=True argument when developing. The running app will restart automatically when code is changed. You don't want to run this in production

We need to create a requirements.txt to log all the packages installed

```bash
pip3 freeze > requirements.txt
```

---
##Run the application
To run the application simply run
```
python3 app.py
```
---
##MongoDB integration

To connect this project to a MongoDB Atlas instance, first install the PyMongo library by running 

```bash 
pip3 install pymongo certifi
``` 
Then, create a MongoDB Atlas account and set up a cluster if you haven't already. Obtain your connection string from the Atlas dashboard. 

In your `app.py` file, import pymongo and establish a connection to your database using the connection string. 

```py
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
```

Update the requirements

```bash
pip3 freeze > requirements.txt
```

Take note of the os.getenv line. It is used to retrieve an environment variable that was set prior to running the web application's execution command.

It's a good practice to create a script file, such as `run.sh`, with the following content:

```bash
export MONGODB_URI="mongodb+srv:/...."
python3 app.py
```

To test the provided Flask API using Postman, follow these steps:

###**Start Your Flask Application**

First, ensure your Flask application is running. You should see output indicating it's running on `http://0.0.0.0:5555`.

###**Open Postman**

Launch Postman and set up the following requests to test each endpoint:

#### **a. GET /**

- **Description**: Retrieve a simple "Hello, World!" message.
- **Method**: `GET`
- **URL**: `http://localhost:5555/`
- **Steps**:
  1. Open Postman.
  2. Set the method to `GET`.
  3. Enter the URL `http://localhost:5555/`.
  4. Click `Send`.
  5. You should receive a response with the message `<p>Hello, World!</p>`.

#### **b. GET /users**

- **Description**: Retrieve a list of users from the database.
- **Method**: `GET`
- **URL**: `http://localhost:5555/users`
- **Steps**:
  1. Set the method to `GET`.
  2. Enter the URL `http://localhost:5555/users`.
  3. Click `Send`.
  4. You should receive a JSON array of users from the database.

#### **c. POST /users**

- **Description**: Insert a new user into the database.
- **Method**: `POST`
- **URL**: `http://localhost:5555/users`
- **Body**:
  - Select `raw` and choose `JSON` format.
  - Provide the user data as a JSON object, e.g.,:
    ```json
    {
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
    ```
- **Steps**:
  1. Set the method to `POST`.
  2. Enter the URL `http://localhost:5555/users`.
  3. Select the `Body` tab.
  4. Choose `raw` and `JSON` from the dropdown.
  5. Enter the JSON data in the text area.
  6. Click `Send`.
  7. You should receive a response with the ID of the inserted user.

#### **d. DELETE /users/{id}**

- **Description**: Delete a user by their ID.
- **Method**: `DELETE`
- **URL**: `http://localhost:5555/users/{id}`
- **Steps**:
  1. Replace `{id}` with the ID of the user you want to delete.
  2. Set the method to `DELETE`.
  3. Enter the URL with the user ID, e.g., `http://localhost:5555/users/1234567890abcdef`.
  4. Click `Send`.
  5. You should receive a response with the count of deleted documents.

#### **e. GET /users/{id}**

- **Description**: Retrieve a single user by their ID.
- **Method**: `GET`
- **URL**: `http://localhost:5555/users/{id}`
- **Steps**:
  1. Replace `{id}` with the ID of the user you want to retrieve.
  2. Set the method to `GET`.
  3. Enter the URL with the user ID, e.g., `http://localhost:5555/users/1234567890abcdef`.
  4. Click `Send`.
  5. You should receive a JSON object with the user's details.

#### **f. PUT /users/{id}**

- **Description**: Update a user's information by their ID.
- **Method**: `PUT`
- **URL**: `http://localhost:5555/users/{id}`
- **Body**:
  - Select `raw` and choose `JSON` format.
  - Provide the updated user data as a JSON object, e.g.,:
    ```json
    {
      "email": "new.email@example.com"
    }
    ```
- **Steps**:
  1. Replace `{id}` with the ID of the user you want to update.
  2. Set the method to `PUT`.
  3. Enter the URL with the user ID, e.g., `http://localhost:5555/users/1234567890abcdef`.
  4. Select the `Body` tab.
  5. Choose `raw` and `JSON` from the dropdown.
  6. Enter the JSON data in the text area.
  7. Click `Send`.
  8. You should receive a response with the count of modified documents.

These steps will help you test each endpoint of your Flask API using Postman effectively.



