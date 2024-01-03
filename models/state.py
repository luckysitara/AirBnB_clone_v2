#!/usr/bin/python3
"""
Module to define the State class.
"""

from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

class State(BaseModel, Base):
    """
    Class representing a State.
    """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """
            Getter method that returns the list of City objects linked
            to the current State.
            """

            cities = []
            for obj in models.storage.all(City).values():
                if obj.state_id == self.id:
                    cities.append(obj)
            return cities

