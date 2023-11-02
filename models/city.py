#!/usr/bin/python3
"""Defines a City class"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represents a city"""

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship(
                'Place',
                backref="cities",
                cascade="all, delete-orphan")
    else:
        @property
        def places(self):
            """Gets the attribute"""
            places = models.storage.all("Place").values()
            return [place for place in places if place.city_id == self.id]
