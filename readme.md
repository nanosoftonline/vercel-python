# Python Web App hosted on Vercel
In this blog we'll create a python project using flask. We'll then show how to create a web application and connect to a MongoDB database

Flask is a micro web framework that is used to build web applications. If you're comming from node, it is very much like the express web framework. You can build an application with a single file

## 1. Create a virtual environment
The virtual environment allows you to create and maintain an isolated project where you can install the packages that re relavent to this project. Within this environment we can then create a requirements.txt which will help when we deploy the project to production.
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
    app.run(host='0.0.0.0', debug=True)

```