#!/usr/bin/python3
""" Amenity Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """ Amenity class, contains a name """

    __tablename__ = 'amenities'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        places = relationship('Place', secondary=place_amenity,
                              back_populates='amenities')
    else:
        name = ""
