#!/usr/bin/python3
"""Defines a FileStorage class"""
import os
import json
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class FileStorage:
    """Represents a data storage class"""

    __file_path = "file.json"
    __objects = {}

    MODELS = {
        "City": City,
        "User": User,
        "Place": Place,
        "State": State,
        "Review": Review,
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        }

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            return {key: obj for key, obj in type(self).__objects.items()
                    if isinstance(obj, cls)}
        return type(self).__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        type(self).__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        objects_dict = {}
        for key, value in type(self).__objects.items():
            objects_dict[key] = value.to_dict()
        with open(type(self).__file_path, "w", encoding="utf-8") as json_file:
            json.dump(objects_dict, json_file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.isfile(type(self).__file_path):
            with open(type(self).__file_path, encoding="utf-8") as json_file:
                objects_dict = json.load(json_file)

            for key, value in objects_dict.items():
                _class_ = value["__class__"]
                type(self).__objects[key] = type(self).MODELS[_class_](**value)

    def delete(self, obj=None):
        """Deletes an obj from __objects"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in type(self).__objects:
                del type(self).__objects[key]
                self.save()

    def close(self):
        """Calls the reload method."""
        self.reload()

    def get(self, cls, id):
        """Returns the object based on the class and its ID,
        or None if not found"""
        key = "{}.{}".format(cls.__name__, id)
        return type(self).__objects.get(key, None)

    def count(self, cls=None):
        """Returns the number of objects in storage
        matching the given class."""
        if cls:
            return len(self.all(cls))
        return len(self.all())
