#!/usr/bin/python3
"""
Create views for Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def amenities():
    """Retrieves the list of all Amenity objects and
    Creates a new Amenity object"""
    if request.method == "GET":
        amenities = [
                amenity.to_dict() for amenity in storage.all(Amenity).values()
                ]
        return jsonify(amenities)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def amenity(amenity_id):
    """Retrieves, Deletes and Updates a Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict())
    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
