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

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, db),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """
        Returns a dictionary of objects of the specified class.
        """
        objects = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for class_name, class_ in Base.classes.items():
                query = self.__session.query(class_).all()
                for obj in query:
                    key = "{}.{}".format(class_name, obj.id)
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


    def reload(self):
        """
        Creates all tables in the database and the current database session.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()


    def close(self):
        """
        Calls remove() method on the private session attribute (self.__session).
        """
        self.__session.close()
