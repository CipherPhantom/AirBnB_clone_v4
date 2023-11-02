#!/usr/bin/python3
"""
Create views for State objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """Return the list of states and Creates a State"""
    if request.method == "GET":
        states = [state.to_dict() for state in storage.all("State").values()]
        return jsonify(states)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def state(state_id):
    """Deletes, Retrieves and Updates a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
