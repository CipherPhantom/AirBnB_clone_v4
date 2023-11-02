#!/usr/bin/python3
"""
This script starts a Flask web application
"""
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """Returns `Hello HBNB!`"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns `HBNB`"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Returns info about the programming language C"""
    return "C {}".format(escape(text).replace("_", " "))


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """Returns info about the programming language Python"""
    return "Python {}".format(escape(text).replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """Return `n is a number`"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Returns H1 tag: “Number: n” inside the tag BODY"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """Returns tag: “Number: n is even|odd” inside the tag BODY"""
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
