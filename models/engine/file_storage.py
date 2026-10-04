#!/usr/bin/python3
"""
Module to define the FileStorage class.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {
    'BaseModel': BaseModel, 'User': User, 'State': State, 'City': City,
    'Place': Place, 'Review': Review, 'Amenity': Amenity
}


class FileStorage:
    """
    Serializes and deserializes instances to/from JSON file.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects, optionally filtered by class.
        """
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls_name = cls
        else:
            cls_name = cls.__name__
        return {key: obj for key, obj in FileStorage.__objects.items()
                if key.split('.')[0] == cls_name}

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to JSON file.
        """
        serialized_objects = {}
        for key, obj in FileStorage.__objects.items():
            serialized_objects[key] = obj.to_dict()

        with open(FileStorage.__file_path, mode='w',
                  encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects if the file exists.
        """
        try:
            with open(FileStorage.__file_path, mode='r',
                      encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    cls = classes.get(key.split('.')[0])
                    if cls is not None:
                        FileStorage.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it is inside.
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects.pop(key, None)

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
        """
        self.reload()
