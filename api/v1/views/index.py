#!/usr/bin/python3
"""Creates views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity


@app_views.route("/status", methods=["GET"])
def status():
    """Return json with status info"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Returns the number of each objects by type"""
    stats = {}
    objects = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    for key, cls in objects.items():
        stats[key] = storage.count(cls)
    return jsonify(stats)
