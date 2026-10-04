#!/usr/bin/python3
"""
Module to define the DBStorage class.
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {
    'User': User, 'State': State, 'City': City, 'Place': Place,
    'Review': Review, 'Amenity': Amenity
}


class DBStorage:
    """
    Database storage class.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Constructor for DBStorage class.
        """
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host, db),
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of objects, filtered by class if given.
        """
        objects = {}
        if cls is None:
            class_list = list(classes.values())
        elif isinstance(cls, str):
            class_list = [classes[cls]]
        else:
            class_list = [cls]
        for class_ in class_list:
            for obj in self.__session.query(class_).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        return objects

    def new(self, obj):
        """
        Adds the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes obj from the current database session if it is not None.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and the current session.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session

    def close(self):
        """
        Calls remove() method on the private session attribute.
        """
        self.__session.remove()
