from flask import Flask

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)

