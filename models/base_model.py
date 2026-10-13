#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key in ('created_at', 'updated_at'):
                    if isinstance(value, str):
                        try:
                            value = datetime.strptime(
                                value, '%Y-%m-%dT%H:%M:%S.%f')
                        except ValueError:
                            value = datetime.strptime(
                                value, '%Y-%m-%dT%H:%M:%S')
                    setattr(self, key, value)
                else:
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with the current time and saves the model"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """Deletes the current instance from the storage"""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Converts the instance into dict format"""
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = (
            str(type(self)).split('.')[-1]).split('\'')[0]
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        if hasattr(self.created_at, 'isoformat'):
            dictionary['created_at'] = self.created_at.isoformat()
        else:
            dictionary['created_at'] = self.created_at
        if hasattr(self.updated_at, 'isoformat'):
            dictionary['updated_at'] = self.updated_at.isoformat()
        else:
            dictionary['updated_at'] = self.updated_at
        return dictionary
