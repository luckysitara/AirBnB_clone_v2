#!/usr/bin/python3
""" Module for testing db storage """
import unittest
from os import getenv
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
import models

try:
    import MySQLdb
    MYSQLDB_INSTALLED = True
except ImportError:
    MYSQLDB_INSTALLED = False


def table_count(table_name):
    """ Counts the records of a table using MySQLdb directly """
    connection = MySQLdb.connect(host=getenv('HBNB_MYSQL_HOST', 'localhost'),
                                 user=getenv('HBNB_MYSQL_USER'),
                                 passwd=getenv('HBNB_MYSQL_PWD'),
                                 db=getenv('HBNB_MYSQL_DB'))
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM {}".format(table_name))
        return cursor.fetchone()[0]
    finally:
        connection.close()


def new_state(name='California'):
    """ Creates a State with the given name """
    state = State()
    state.name = name
    return state


def new_user(email='airbnb@mail.com', password='root'):
    """ Creates a User with the given credentials """
    user = User()
    user.email = email
    user.password = password
    return user


def new_city(state, name='San Francisco'):
    """ Creates a City linked to the given State """
    city = City()
    city.state_id = state.id
    city.name = name
    return city


def new_place(city, user, name='Hbnb'):
    """ Creates a Place linked to the given City and User """
    place = Place()
    place.city_id = city.id
    place.user_id = user.id
    place.name = name
    return place


def new_review(place, user, text='Great place'):
    """ Creates a Review linked to the given Place and User """
    review = Review()
    review.place_id = place.id
    review.user_id = user.id
    review.text = text
    return review


@unittest.skipUnless(models.storage_t == 'db', "Test suite for DBStorage")
class test_dbStorage(unittest.TestCase):
    """ Class to test the db storage method """

    def tearDown(self):
        """ Closes the current session """
        models.storage.close()

    def test_storage_var_created(self):
        """ DBStorage object storage created """
        self.assertEqual(type(models.storage), DBStorage)

    def test_all(self):
        """ __objects is properly returned """
        self.assertIsInstance(models.storage.all(), dict)

    def test_new(self):
        """ New object is correctly added to the storage """
        state = new_state()
        models.storage.new(state)
        self.assertIn('State.{}'.format(state.id), models.storage.all())

    def test_save(self):
        """ Data is saved to the storage """
        state = new_state()
        state.save()
        self.assertIn('State.{}'.format(state.id), models.storage.all())

    def test_delete(self):
        """ Object is removed from the storage """
        state = new_state()
        state.save()
        key = 'State.{}'.format(state.id)
        models.storage.delete(state)
        models.storage.save()
        self.assertNotIn(key, models.storage.all())

    def test_delete_none(self):
        """ Deleting None does not raise an error """
        models.storage.delete()
        models.storage.delete(None)

    def test_all_with_class(self):
        """ Objects are filtered by class """
        state = new_state()
        state.save()
        user = new_user()
        user.save()
        states = models.storage.all(State)
        self.assertIn('State.{}'.format(state.id), states)
        self.assertNotIn('User.{}'.format(user.id), states)

    def test_all_with_class_name(self):
        """ Objects are filtered by class name """
        state = new_state()
        state.save()
        states = models.storage.all('State')
        self.assertIn('State.{}'.format(state.id), states)

    def test_reload(self):
        """ Objects are still available after a reload """
        state = new_state()
        state.save()
        models.storage.reload()
        self.assertIn('State.{}'.format(state.id), models.storage.all())

    def test_close(self):
        """ Session is closed and can be recreated """
        models.storage.close()
        self.assertIsInstance(models.storage.all(), dict)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_save_adds_state_record(self):
        """ Saving a State adds a record in the states table """
        before = table_count('states')
        new_state().save()
        self.assertEqual(table_count('states'), before + 1)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_save_adds_user_record(self):
        """ Saving a User adds a record in the users table """
        before = table_count('users')
        new_user().save()
        self.assertEqual(table_count('users'), before + 1)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_save_adds_amenity_record(self):
        """ Saving an Amenity adds a record in the amenities table """
        before = table_count('amenities')
        amenity = Amenity()
        amenity.name = 'Wifi'
        amenity.save()
        self.assertEqual(table_count('amenities'), before + 1)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_save_adds_city_record(self):
        """ Saving a City adds a record in the cities table """
        state = new_state()
        state.save()
        before = table_count('cities')
        new_city(state).save()
        self.assertEqual(table_count('cities'), before + 1)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_save_adds_place_record(self):
        """ Saving a Place adds a record in the places table """
        state = new_state()
        state.save()
        city = new_city(state)
        city.save()
        user = new_user()
        user.save()
        before = table_count('places')
        new_place(city, user).save()
        self.assertEqual(table_count('places'), before + 1)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_save_adds_review_record(self):
        """ Saving a Review adds a record in the reviews table """
        state = new_state()
        state.save()
        city = new_city(state)
        city.save()
        user = new_user()
        user.save()
        place = new_place(city, user)
        place.save()
        before = table_count('reviews')
        new_review(place, user).save()
        self.assertEqual(table_count('reviews'), before + 1)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_delete_removes_record(self):
        """ Deleting an object removes its record from the table """
        state = new_state('Oregon')
        state.save()
        before = table_count('states')
        models.storage.delete(state)
        models.storage.save()
        self.assertEqual(table_count('states'), before - 1)

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_state_cities_relationship(self):
        """ A State is linked to its City through the db relationship """
        state = new_state()
        state.save()
        city = new_city(state)
        city.save()
        self.assertIn(city.id, [obj.id for obj in state.cities])

    @unittest.skipUnless(MYSQLDB_INSTALLED, "MySQLdb is not installed")
    def test_place_amenity_relationship(self):
        """ A Place and an Amenity are linked through place_amenity """
        state = new_state()
        state.save()
        city = new_city(state)
        city.save()
        user = new_user()
        user.save()
        place = new_place(city, user)
        place.save()
        amenity = Amenity()
        amenity.name = 'Wifi'
        amenity.save()
        before = table_count('place_amenity')
        place.amenities.append(amenity)
        place.save()
        self.assertEqual(table_count('place_amenity'), before + 1)
        self.assertIn(amenity.id, [obj.id for obj in place.amenities])
        self.assertIn(place.id, [obj.id for obj in amenity.places])


if __name__ == '__main__':
    unittest.main()
