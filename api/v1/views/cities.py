#!/usr/bin/python3
"""
Create views for City objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def state_cities(state_id):
    """Retrieves the list of all City objects of a State and
    Creates a City object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        data["state_id"] = state_id
        city = City(**data)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def city(city_id):
    """Retrieves, Updates and Deletes a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
