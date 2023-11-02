#!/usr/bin/python3
"""Defines an Amenity class"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Represents an amenity"""

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship(
                "Place",
                secondary=place_amenity,
                back_populates="amenities"
                )
