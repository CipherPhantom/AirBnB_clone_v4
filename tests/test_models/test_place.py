#!/usr/bin/python3
"""
Unittest for models.place([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import json
import datetime
import models.place
from io import StringIO
from models.place import Place
from models.amenity import Amenity
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from unittest.mock import patch, mock_open


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
def setUpModule():
    FileStorage._FileStorage__objects = {}


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
def tearDownModule():
    FileStorage._FileStorage__objects = {}
    if os.path.exists("file.json"):
        os.remove("file.json")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestAllPlaceDocstrings(unittest.TestCase):
    def setUp(self):
        self.p0 = Place()

    def testModuleDocstring(self):
        self.assertGreater(len(models.place.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.place, "Place"))
        self.assertGreater(len(Place.__doc__), 1)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestPlaceClass(unittest.TestCase):
    def setUp(self):
        self.p0 = Place()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.p0, BaseModel)

    def test_SubClass(self):
        self.assertTrue(issubclass(Place, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.p0.id, None)
        self.assertEqual(self.p0.id, str(uuid.UUID(self.p0.id)))

    def test_InstanceVariable(self):
        self.assertNotEqual(type(Place.name), str)
        self.assertNotEqual(type(Place.created_at), datetime.datetime)
        self.assertNotEqual(type(Place.updated_at), datetime.datetime)

    def test_createdAt(self):
        self.assertIsNot(self.p0.created_at, None)
        self.assertEqual(type(self.p0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.p0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.p0.updated_at, None)
        self.assertEqual(type(self.p0.updated_at), datetime.datetime)
        self.assertLess((self.p0.updated_at - self.p0.created_at).
                        total_seconds(), 0.001)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestPlaceClassAttributes(unittest.TestCase):
    def setUp(self):
        self.c_id = str(uuid.uuid4())
        self.u_id = str(uuid.uuid4())
        self.p0 = Place(city_id=self.c_id, user_id=self.u_id, name="La Casa",
                        description="Mountain and Ocean View",
                        number_rooms=7, number_bathrooms=4,
                        max_guest=10, price_by_night=200,
                        latitude=2.5, longitude=2.31
                        )

    def testCityIdAttribute(self):
        self.assertEqual(self.p0.city_id, self.c_id)

    def testUserIdAttribute(self):
        self.assertEqual(self.p0.user_id, self.u_id)

    def testNameAttribute(self):
        self.assertEqual(self.p0.name, "La Casa")

    def testDescriptionAttribute(self):
        self.assertEqual(self.p0.description, "Mountain and Ocean View")

    def testNumberRoomsAttribute(self):
        self.assertEqual(self.p0.number_rooms, 7)

    def testNumberBathroomsAttribute(self):
        self.assertEqual(self.p0.number_bathrooms, 4)

    def testMaxGuestAttribute(self):
        self.assertEqual(self.p0.max_guest, 10)

    def testPriceByNightAttribute(self):
        self.assertEqual(self.p0.price_by_night, 200)

    def testLatitudeAttribute(self):
        self.assertEqual(self.p0.latitude, 2.5)

    def testLongitudeAttribute(self):
        self.assertEqual(self.p0.longitude, 2.31)

    def testAmenityIdsAttribute(self):
        a0 = Amenity(name="Wifi")
        self.p0.amenities.append(a0)
        self.assertEqual(self.p0.amenities[0].id, a0.id)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestStrMethod(unittest.TestCase):
    def testStr(self):
        p1 = Place()
        p1.city_id = str(uuid.uuid4())
        p1.user_id = str(uuid.uuid4())
        p1.name = "Casa Rodolfo"
        p1.description = "Cozy penthouse with beautiful land view"
        p1.number_rooms = 2
        p1.number_bathrooms = 2
        p1.max_guest = 4
        p1.price_by_night = 138
        p1.latitude = 5.734
        p1.longitude = 10.2456

        p1_dict_copy = p1.__dict__.copy()
        if '_sa_instance_state' in p1_dict_copy:
            del p1_dict_copy['_sa_instance_state']
        self.assertEqual(str(p1), "[{}] ({}) {}".format(
                         type(p1).__name__, p1.id, p1_dict_copy))

    def testPrint(self):
        p1 = Place()
        p1.city_id = str(uuid.uuid4())
        p1.user_id = str(uuid.uuid4())
        p1.name = "Drago Apartment"
        p1.description = "Exclusive Apartments"
        p1.number_rooms = 1
        p1.number_bathrooms = 1
        p1.max_guest = 2
        p1.price_by_night = 102
        p1.latitude = 31.4567
        p1.longitude = 15.3426
        p1.amenity_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(p1)
            self.assertEqual(mock_print.getvalue(), "{}\n".format(str(p1)))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        p1 = Place()
        prev_time = p1.updated_at
        p1.save()
        self.assertEqual(type(p1.updated_at), datetime.datetime)
        self.assertGreater(p1.updated_at, prev_time)

    def testSaveToStorage(self):
        p1 = Place()
        prev_time = p1.updated_at
        fname = "file.json"

        with patch('models.storage.new') as m:
            with patch("models.engine.file_storage.open", mock_open()) as mk_f:
                p1.save()
                mk_f.assert_called_once_with(fname, 'w', encoding='utf-8')
                self.assertEqual(m.call_args.args, (p1, ))
                FileStorage._FileStorage__objects = {}

        self.assertEqual(type(p1.updated_at), datetime.datetime)
        self.assertGreater(p1.updated_at, prev_time)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        p1 = Place()
        self.assertEqual(p1.to_dict(),
                         {'__class__': 'Place',
                          'updated_at': '{}'.format(p1.updated_at.isoformat()),
                          'created_at': '{}'.format(p1.created_at.isoformat()),
                          'id': p1.id})

    def testToDictionary2(self):
        p1 = Place()
        p1.city_id = str(uuid.uuid4())
        p1.name = "The Squire's Field"
        p1.number_rooms = 12
        p1.price_by_night = 133
        p1.latitude = 15.6781
        p1.longitude = 2.345
        self.assertEqual(p1.to_dict(),
                         {'__class__': 'Place',
                          'updated_at': '{}'.format(p1.updated_at.isoformat()),
                          'created_at': '{}'.format(p1.created_at.isoformat()),
                          'id': p1.id,
                          'city_id': p1.city_id,
                          'name': "The Squire's Field",
                          'number_rooms': 12,
                          'price_by_night': 133,
                          'longitude': 2.345,
                          'latitude': 15.6781})

    def testToDictInvalidArg(self):
        p1 = Place()
        with self.assertRaises(TypeError):
            p1.to_dict(5)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestPlaceFromDict(unittest.TestCase):
    def testRecreate(self):
        p1 = Place()
        p1_dict = p1.to_dict()

        with patch('models.storage.new') as m:
            p2 = Place(**p1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(p1_dict, p2.to_dict())
        self.assertIsNot(p1, p2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "Place",
                     'name': "Beachfront aparte",
                     'description': "Heart of Lekki/V.I",
                     'number_rooms': 2,
                     'number_bathrooms': 2,
                     'amenity_ids': [str(uuid.uuid4())],
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        p1 = Place(**cust_dict)
        self.assertEqual(p1.to_dict(), cust_dict)
        self.assertEqual(type(p1.updated_at), datetime.datetime)
        self.assertGreater(p1.updated_at, p1.created_at)
        self.assertEqual(p1.name, "Beachfront aparte")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        p1 = Place("test", "kwargs", unused_id, unused_date)
        self.assertEqual(p1.to_dict(),
                         {'__class__': 'Place',
                          'updated_at': '{}'.format(p1.updated_at.isoformat()),
                          'created_at': '{}'.format(p1.created_at.isoformat()),
                          'id': p1.id})
        self.assertNotEqual(p1.id, unused_id)
        self.assertNotEqual(p1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        p1 = Place()
        p1_dict = p1.to_dict()

        p2 = Place("test", str(uuid.uuid4()),
                   datetime.datetime.now(), **p1_dict)
        self.assertEqual(p1_dict, p2.to_dict())
        self.assertIsNot(p1, p2)
