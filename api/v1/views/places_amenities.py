#!/usr/bin/python3
"""
Create views for the link between Place objects and Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
import os


@app_views.route("places/<place_id>/amenities", methods=["GET"])
def place_amenites(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        amenities = []
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            amenities = [
                    amenity.to_dict() for amenity in place.amenities
                    ]
        else:
            for amenity_id in place.amenities:
                amenity = storage.get("Amenity", amenity_id)
                if amenity:
                    amenities.append(amenity.to_dict())
        return jsonify(amenities)


@app_views.route(
        "places/<place_id>/amenities/<amenity_id>",
        methods=["DELETE", "POST"])
def place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place and
    Link a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "DELETE":
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity not in place.amenities:
                abort(404)
            else:
                place.amenities.remove(amenity)
                storage.save()
        else:
            if amenity_id not in place.amenities:
                abort(404)
            else:
                place.amenities.remove(amenity_id)
                storage.save()
        return jsonify({}), 200
    if request.method == "POST":
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
            storage.save()
        else:
            if amenity_id in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities = amenity
            storage.save()
        return jsonify(amenity.to_dict()), 201
