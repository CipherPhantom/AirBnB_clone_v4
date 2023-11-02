#!/usr/bin/python3
"""Defines a Place class"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False))


class Place(BaseModel, Base):
    """Represents a place"""

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
                "Review",
                backref="place",
                cascade="all, delete-orphan")
        amenities = relationship(
                "Amenity",
                secondary=place_amenity,
                viewonly=False,
                back_populates="place_amenities"
                )
    else:
        @property
        def reviews(self):
            """Gets the attribute"""
            reviews = models.storage.all("Review").values()
            return [review for review in reviews if review.place_id == self.id]

        @property
        def amenities(self):
            """"Gets the attribute"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """Sets the attribute"""
            if isinstance(obj, models.MODELS["Amenity"]) and \
                    obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
