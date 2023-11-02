#!/usr/bin/python3
"""
Unittest for models.amenity([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import datetime
import json
import models.amenity
from io import StringIO
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
class TestAllAmenityDocstrings(unittest.TestCase):
    def setUp(self):
        self.a0 = Amenity()

    def testModuleDocstring(self):
        self.assertGreater(len(models.amenity.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.amenity, "Amenity"))
        self.assertGreater(len(Amenity.__doc__), 1)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestAmenityClass(unittest.TestCase):
    def setUp(self):
        self.a0 = Amenity()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.a0, Amenity)

    def test_SubClass(self):
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.a0.id, None)
        self.assertEqual(self.a0.id, str(uuid.UUID(self.a0.id)))

    def test_InstanceVariable(self):
        self.assertNotEqual(type(Amenity.id), str)
        self.assertNotEqual(type(Amenity.created_at), datetime.datetime)
        self.assertNotEqual(type(Amenity.updated_at), datetime.datetime)

    def test_createdAt(self):
        self.assertIsNot(self.a0.created_at, None)
        self.assertEqual(type(self.a0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.a0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.a0.updated_at, None)
        self.assertEqual(type(self.a0.updated_at), datetime.datetime)
        self.assertLess((self.a0.updated_at - self.a0.created_at).
                        total_seconds(), 0.001)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestAmenityClassAttributes(unittest.TestCase):
    def testNameAttribute(self):
        a1 = Amenity(name="Pool")
        self.assertEqual(type(a1.name), str)
        self.assertEqual(a1.name, "Pool")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestStrMethod(unittest.TestCase):
    def testStr(self):
        a1 = Amenity()
        a1.name = "Garden"

        a1_dict_copy = a1.__dict__.copy()
        if '_sa_instance_state' in a1_dict_copy:
            del a1_dict_copy['_sa_instance_state']
        self.assertEqual(str(a1), "[{}] ({}) {}".format(
                         type(a1).__name__, a1.id, a1_dict_copy))

    def testPrint(self):
        a1 = Amenity()
        a1.name = "Jacuzzi"
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(a1)
            self.assertEqual(mock_print.getvalue(), "{}\n".format(str(a1)))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        a1 = Amenity()
        prev_time = a1.updated_at
        a1.save()
        self.assertEqual(type(a1.updated_at), datetime.datetime)
        self.assertGreater(a1.updated_at, prev_time)

    def testSaveToStorage(self):
        a1 = Amenity()
        a1.name = "Garage"
        prev_time = a1.updated_at
        fname = "file.json"
        with patch("models.engine.file_storage.open", mock_open()) as mk_f:
            a1.save()
            mk_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(a1.updated_at), datetime.datetime)
        self.assertGreater(a1.updated_at, prev_time)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        a1 = Amenity()
        self.assertEqual(a1.to_dict(),
                         {'__class__': 'Amenity',
                          'updated_at': '{}'.format(a1.updated_at.isoformat()),
                          'created_at': '{}'.format(a1.created_at.isoformat()),
                          'id': a1.id})

    def testToDictionary2(self):
        a1 = Amenity()
        a1.name = "Electric Gate"
        self.assertEqual(a1.to_dict(),
                         {'__class__': 'Amenity',
                          'updated_at': '{}'.format(a1.updated_at.isoformat()),
                          'created_at': '{}'.format(a1.created_at.isoformat()),
                          'id': a1.id,
                          'name': 'Electric Gate'})

    def testToDictInvalidArg(self):
        a1 = Amenity()
        with self.assertRaises(TypeError):
            a1.to_dict(5)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestBaseModelFromDict(unittest.TestCase):
    def testRecreate(self):
        a1 = Amenity()
        a1_dict = a1.to_dict()

        with patch('models.storage.new') as m:
            a2 = Amenity(**a1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(a1_dict, a2.to_dict())
        self.assertIsNot(a1, a2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "Amenity",
                     'name': "Alexa",
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        a1 = Amenity(**cust_dict)
        self.assertEqual(a1.to_dict(), cust_dict)
        self.assertEqual(type(a1.updated_at), datetime.datetime)
        self.assertGreater(a1.updated_at, a1.created_at)
        self.assertEqual(a1.name, "Alexa")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        a1 = Amenity("test", "kwargs", unused_id, unused_date)
        self.assertEqual(a1.to_dict(),
                         {'__class__': 'Amenity',
                          'updated_at': '{}'.format(a1.updated_at.isoformat()),
                          'created_at': '{}'.format(a1.created_at.isoformat()),
                          'id': a1.id})
        self.assertNotEqual(a1.id, unused_id)
        self.assertNotEqual(a1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        a1 = BaseModel()
        a1_dict = a1.to_dict()

        a2 = BaseModel("test", str(uuid.uuid4()),
                       datetime.datetime.now(), **a1_dict)
        self.assertEqual(a1_dict, a2.to_dict())
        self.assertEqual(a1.__dict__, a2.__dict__)
        self.assertIsNot(a1, a2)
