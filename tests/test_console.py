#!/usr/bin/python3
""" Unit tests for the HBNB console """
import ast
import contextlib
import io
import os
import unittest
from uuid import UUID
from console import HBNBCommand
import models

storage = models.storage


@unittest.skipIf(models.storage_t == 'db', "Test suite for FileStorage")
class TestConsole(unittest.TestCase):
    """ Tests the commands of the HBNB console """

    def setUp(self):
        """ Clears the storage and creates a console instance """
        self.console = HBNBCommand()
        self.clear_storage()

    def tearDown(self):
        """ Clears the storage and removes the JSON file """
        self.clear_storage()
        try:
            os.remove('file.json')
        except OSError:
            pass

    @staticmethod
    def clear_storage():
        """ Removes every object from the file storage """
        for key in list(storage.all().keys()):
            del storage._FileStorage__objects[key]

    def run_command(self, command):
        """ Runs a command and returns everything printed to stdout """
        output = io.StringIO()
        self.console.stdout = output
        with contextlib.redirect_stdout(output):
            self.console.onecmd(self.console.precmd(command))
        return output.getvalue()

    def create(self, class_name='BaseModel'):
        """ Creates an object and returns its id """
        return self.run_command('create {}'.format(class_name)).strip()

    def test_create(self):
        """ create prints the id of the new instance """
        UUID(self.create())

    def test_create_adds_object(self):
        """ create adds the instance to the storage """
        obj_id = self.create()
        self.assertIn('BaseModel.{}'.format(obj_id), storage.all())

    def test_create_every_class(self):
        """ create works for every class of the console """
        for class_name in ['BaseModel', 'User', 'Place', 'State', 'City',
                           'Amenity', 'Review']:
            UUID(self.create(class_name))

    def test_create_missing_class_name(self):
        """ create without arguments """
        self.assertEqual(self.run_command('create').strip(),
                         '** class name missing **')

    def test_create_unknown_class(self):
        """ create with an unknown class """
        self.assertEqual(self.run_command('create Nope').strip(),
                         "** class doesn't exist **")

    def test_create_with_parameters(self):
        """ create sets the attributes given as parameters """
        obj_id = self.run_command(
            'create Place city_id="0001" user_id="0001" '
            'name="My_little_house" number_rooms=4 number_bathrooms=2 '
            'max_guest=10 price_by_night=300 latitude=37.773972 '
            'longitude=-122.431297').strip()
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.city_id, '0001')
        self.assertEqual(obj.user_id, '0001')
        self.assertEqual(obj.name, 'My little house')
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 10)
        self.assertEqual(obj.price_by_night, 300)
        self.assertEqual(obj.latitude, 37.773972)
        self.assertEqual(obj.longitude, -122.431297)

    def test_create_string_parameter(self):
        """ a quoted value is set as a string """
        obj_id = self.run_command('create State name="California"').strip()
        self.assertEqual(storage.all()['State.' + obj_id].name, 'California')

    def test_create_parameter_underscores(self):
        """ underscores of a quoted value are replaced by spaces """
        obj_id = self.run_command(
            'create Place name="My_little_house"').strip()
        self.assertEqual(storage.all()['Place.' + obj_id].name,
                         'My little house')

    def test_create_parameter_escaped_quotes(self):
        """ escaped double quotes of a quoted value are restored """
        obj_id = self.run_command(
            'create Place name="My_\\"little\\"_house"').strip()
        self.assertEqual(storage.all()['Place.' + obj_id].name,
                         'My "little" house')

    def test_create_quoted_number_parameter(self):
        """ a quoted number is set as a string """
        obj_id = self.run_command('create Place city_id="0001"').strip()
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.city_id, '0001')
        self.assertEqual(type(obj.city_id), str)

    def test_create_integer_parameter(self):
        """ a value without a dot is set as an integer """
        obj_id = self.run_command('create Place number_rooms=4').strip()
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(type(obj.number_rooms), int)

    def test_create_float_parameter(self):
        """ a value with a dot is set as a float """
        obj_id = self.run_command('create Place latitude=37.773972').strip()
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.latitude, 37.773972)
        self.assertEqual(type(obj.latitude), float)

    def test_create_negative_float_parameter(self):
        """ a negative value with a dot is set as a float """
        obj_id = self.run_command(
            'create Place longitude=-122.431297').strip()
        self.assertEqual(storage.all()['Place.' + obj_id].longitude,
                         -122.431297)

    def test_create_skips_invalid_parameters(self):
        """ parameters that cannot be cast are skipped """
        obj_id = self.run_command(
            'create Place zodiac=xyz name="Valid"').strip()
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.name, 'Valid')
        self.assertFalse(hasattr(obj, 'zodiac'))

    def test_create_skips_parameters_without_equal_sign(self):
        """ parameters without an equal sign are skipped """
        obj_id = self.run_command(
            'create State name="Arizona" invalid').strip()
        self.assertEqual(storage.all()['State.' + obj_id].name, 'Arizona')

    def test_create_skips_empty_value(self):
        """ a parameter with an empty value is skipped """
        obj_id = self.run_command('create State name=').strip()
        self.assertEqual(storage.all()['State.' + obj_id].name, '')

    def test_show(self):
        """ show displays the requested instance """
        obj_id = self.create()
        output = self.run_command('show BaseModel {}'.format(obj_id))
        self.assertIn('[BaseModel] ({})'.format(obj_id), output)

    def test_show_missing_class_name(self):
        """ show without arguments """
        self.assertEqual(self.run_command('show').strip(),
                         '** class name missing **')

    def test_show_unknown_class(self):
        """ show with an unknown class """
        self.assertEqual(self.run_command('show Nope 123').strip(),
                         "** class doesn't exist **")

    def test_show_missing_id(self):
        """ show with a missing id """
        self.assertEqual(self.run_command('show BaseModel').strip(),
                         '** instance id missing **')

    def test_show_unknown_id(self):
        """ show with an unknown id """
        self.assertEqual(self.run_command('show BaseModel 123').strip(),
                         '** no instance found **')

    def test_destroy(self):
        """ destroy removes the requested instance """
        obj_id = self.create()
        self.run_command('destroy BaseModel {}'.format(obj_id))
        self.assertNotIn('BaseModel.{}'.format(obj_id), storage.all())

    def test_destroy_missing_id(self):
        """ destroy with a missing id """
        self.assertEqual(self.run_command('destroy BaseModel').strip(),
                         '** instance id missing **')

    def test_destroy_unknown_id(self):
        """ destroy with an unknown id """
        self.assertEqual(self.run_command('destroy BaseModel 123').strip(),
                         '** no instance found **')

    def test_destroy_unknown_class(self):
        """ destroy with an unknown class """
        self.assertEqual(self.run_command('destroy Nope 123').strip(),
                         "** class doesn't exist **")

    def test_all_empty(self):
        """ all prints an empty list when the storage is empty """
        self.assertEqual(self.run_command('all').strip(), '[]')

    def test_all(self):
        """ all prints every instance of the storage """
        self.create()
        self.create('User')
        self.assertEqual(len(ast.literal_eval(self.run_command('all'))), 2)

    def test_all_class(self):
        """ all prints only the instances of the given class """
        self.create()
        self.create('User')
        output = ast.literal_eval(self.run_command('all User'))
        self.assertEqual(len(output), 1)
        self.assertIn('[User]', output[0])

    def test_all_unknown_class(self):
        """ all with an unknown class """
        self.assertEqual(self.run_command('all Nope').strip(),
                         "** class doesn't exist **")

    def test_count(self):
        """ count prints the number of instances of a class """
        self.create()
        self.create()
        self.create('User')
        self.assertEqual(self.run_command('count BaseModel').strip(), '2')

    def test_count_empty(self):
        """ count prints 0 when there is no instance """
        self.assertEqual(self.run_command('count BaseModel').strip(), '0')

    def test_update_attribute(self):
        """ update changes an attribute of an instance """
        obj_id = self.create()
        self.run_command('update BaseModel {} name Holberton'.format(obj_id))
        self.assertEqual(storage.all()['BaseModel.' + obj_id].name,
                         'Holberton')

    def test_update_typed_attribute(self):
        """ update casts attributes that have a known type """
        obj_id = self.create('Place')
        self.run_command('update Place {} number_rooms 4'.format(obj_id))
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.number_rooms, 4)

    def test_update_dict(self):
        """ update accepts a dictionary of attributes """
        obj_id = self.create('Place')
        self.run_command('update Place {} {{"number_rooms": 3, '
                         '"max_guest": 5}}'.format(obj_id))
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.number_rooms, 3)
        self.assertEqual(obj.max_guest, 5)

    def test_update_missing_attribute_name(self):
        """ update without an attribute name """
        obj_id = self.create()
        self.assertEqual(self.run_command('update BaseModel {}'.format(
            obj_id)).strip(), '** attribute name missing **')

    def test_update_missing_value(self):
        """ update without a value """
        obj_id = self.create()
        self.assertEqual(self.run_command('update BaseModel {} name'.format(
            obj_id)).strip(), '** value missing **')

    def test_update_unknown_instance(self):
        """ update an unknown instance """
        self.assertEqual(self.run_command('update BaseModel 123 name x'
                                          ).strip(), '** no instance found **')

    def test_dot_all(self):
        """ <class>.all() prints the instances of the class """
        self.create()
        self.create('User')
        output = ast.literal_eval(self.run_command('User.all()'))
        self.assertEqual(len(output), 1)
        self.assertIn('[User]', output[0])

    def test_dot_count(self):
        """ <class>.count() prints the number of instances """
        self.create()
        self.assertEqual(self.run_command('BaseModel.count()').strip(), '1')

    def test_dot_show(self):
        """ <class>.show(<id>) displays the instance """
        obj_id = self.create()
        output = self.run_command('BaseModel.show("{}")'.format(obj_id))
        self.assertIn('[BaseModel] ({})'.format(obj_id), output)

    def test_dot_update(self):
        """ <class>.update(<id>, <attribute>, <value>) updates the instance """
        obj_id = self.create()
        self.run_command('BaseModel.update("{}", "name", "Holberton")'.format(
            obj_id))
        self.assertEqual(storage.all()['BaseModel.' + obj_id].name,
                         'Holberton')

    def test_dot_update_dict(self):
        """ <class>.update(<id>, <dictionary>) updates the instance """
        obj_id = self.create('Place')
        self.run_command('Place.update("{}", {{"max_guest": 2}})'.format(
            obj_id))
        self.assertEqual(storage.all()['Place.' + obj_id].max_guest, 2)

    def test_dot_destroy(self):
        """ <class>.destroy(<id>) removes the instance """
        obj_id = self.create()
        self.run_command('BaseModel.destroy("{}")'.format(obj_id))
        self.assertNotIn('BaseModel.{}'.format(obj_id), storage.all())

    def test_dot_unknown_command(self):
        """ an unknown dot command is rejected """
        self.assertIn('*** Unknown syntax',
                      self.run_command('BaseModel.nope()'))

    def test_emptyline(self):
        """ an empty line does nothing """
        self.assertEqual(self.run_command(''), '')

    def test_quit(self):
        """ quit exits the console """
        with self.assertRaises(SystemExit):
            self.run_command('quit')

    def test_eof(self):
        """ EOF exits the console """
        with self.assertRaises(SystemExit):
            self.run_command('EOF')


if __name__ == '__main__':
    unittest.main()
