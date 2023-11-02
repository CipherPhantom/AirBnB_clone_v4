#!/usr/bin/python3
"""
This script starts a Flask web application
"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    """Renderd States and state"""
    state = None
    states = storage.all("State").values()
    for s in states:
        if s.id == id:
            state = s
    return render_template("9-states.html", states=states, id=id, state=state)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
