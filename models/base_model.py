#!/usr/bin/python3
"""Defines a BaseModel class"""
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv


Base = declarative_base()


class BaseModel:
    """Represent the base class"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initializes the an instance of BaseModel"""
        if kwargs:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key != "__class__":
                    try:
                        value = datetime.strptime(str(value), date_format)
                    except ValueError:
                        pass
                    setattr(self, key, value)
                if "id" not in kwargs:
                    self.id = str(uuid.uuid4())
                if "created_at" not in kwargs:
                    self.created_at = self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def save(self):
        """Updates the updated_at attribute with the current time"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary of the instance"""
        attributes = self.__dict__.copy()
        attributes["__class__"] = type(self).__name__

        if "_sa_instance_state" in attributes:
            del attributes["_sa_instance_state"]

        if getenv("HBNB_TYPE_STORAGE") == "db" and "password" in attributes:
            del attributes["password"]

        for key, value in attributes.items():
            if isinstance(value, datetime):
                attributes[key] = value.isoformat()

        return attributes

    def delete(self):
        """Deletes itself from storage"""
        models.storage.delete(self)

    def __str__(self):
        """Returns the string representation of the instance"""

        attributes = self.__dict__.copy()
        if "_sa_instance_state" in attributes:
            del attributes["_sa_instance_state"]

        return "[{}] ({}) {}".format(type(self).__name__, self.id, attributes)
