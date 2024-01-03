#!/usr/bin/python3
"""
Module to define the FileStorage class.
"""

import json
from models.base_model import BaseModel

class FileStorage:
    """
    Serializes and deserializes instances to/from JSON file.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects.
        """
        return FileStorage.__objects

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

        with open(FileStorage.__file_path, mode='w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(FileStorage.__file_path, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    cls_name, obj_id = key.split('.')
                    cls = [subcls for subcls in BaseModel.__subclasses__() if subcls.__name__ == cls_name]
                    if cls:
                        obj = cls[0](**value)
                        FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects.
        """
        self.reload()

