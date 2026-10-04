#!/usr/bin/python3
"""
Module to define the State class.
"""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """
    Class representing a State.
    """

    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            """
            Getter method that returns the list of City objects linked
            to the current State.
            """
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
