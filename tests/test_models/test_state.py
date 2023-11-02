#!/usr/bin/python3
"""
Unittest for models.state([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import datetime
import json
import models.state
from io import StringIO
from models.state import State
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
class TestAllStateDocstrings(unittest.TestCase):
    def setUp(self):
        self.s0 = State()

    def testModuleDocstring(self):
        self.assertGreater(len(models.state.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.state, "State"))
        self.assertGreater(len(State.__doc__), 1)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestStateClass(unittest.TestCase):
    def setUp(self):
        self.s0 = State()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.s0, State)

    def test_SubClass(self):
        self.assertTrue(issubclass(State, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.s0.id, None)
        self.assertEqual(self.s0.id, str(uuid.UUID(self.s0.id)))

    def test_InstanceVariable(self):
        self.assertNotEqual(type(State), str)
        self.assertNotEqual(type(State.created_at), datetime.datetime)
        self.assertNotEqual(type(State.updated_at), datetime.datetime)

    def test_createdAt(self):
        self.assertIsNot(self.s0.created_at, None)
        self.assertEqual(type(self.s0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.s0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.s0.updated_at, None)
        self.assertEqual(type(self.s0.updated_at), datetime.datetime)
        self.assertLess((self.s0.updated_at - self.s0.created_at).
                        total_seconds(), 0.001)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestStateClassAttributes(unittest.TestCase):
    def testNameAttribute(self):
        s1 = State(name="LA")
        self.assertEqual(s1.name, "LA")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestStrMethod(unittest.TestCase):
    def testStr(self):
        s1 = State()
        s1.name = "Kigali"
        s1_dict_copy = s1.__dict__.copy()
        if '_sa_instance_state' in s1_dict_copy:
            del s1_dict_copy['_sa_instance_state']
        self.assertEqual(str(s1), "[{}] ({}) {}".format(
                         type(s1).__name__, s1.id, s1_dict_copy))

    def testPrint(self):
        s1 = State()
        s1.name = "Kampala"
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(s1)
            self.assertEqual(mock_print.getvalue(), "{}\n".format(str(s1)))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        s1 = State()
        prev_time = s1.updated_at
        fname = "file.json"

        with patch('models.storage.new') as m:
            with patch("models.engine.file_storage.open", mock_open()) as mk_f:
                s1.save()
                mk_f.assert_called_once_with(fname, 'w', encoding='utf-8')
                self.assertEqual(m.call_args.args, (s1, ))
                FileStorage._FileStorage__objects = {}

        self.assertEqual(type(s1.updated_at), datetime.datetime)
        self.assertGreater(s1.updated_at, prev_time)

    def testSaveToStorage(self):
        s1 = State()
        prev_time = s1.updated_at
        fname = "file.json"
        with patch("models.engine.file_storage.open", mock_open()) as mock_f:
            s1.save()
            mock_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(s1.updated_at), datetime.datetime)
        self.assertGreater(s1.updated_at, prev_time)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        s1 = State()
        self.assertEqual(s1.to_dict(),
                         {'__class__': 'State',
                          'updated_at': '{}'.format(s1.updated_at.isoformat()),
                          'created_at': '{}'.format(s1.created_at.isoformat()),
                          'id': s1.id})

    def testToDictionary2(self):
        s1 = State()
        s1.name = "Texas"
        self.assertEqual(s1.to_dict(),
                         {'__class__': 'State',
                          'updated_at': '{}'.format(s1.updated_at.isoformat()),
                          'created_at': '{}'.format(s1.created_at.isoformat()),
                          'id': s1.id,
                          'name': 'Texas'})

    def testToDictInvalidArg(self):
        s1 = State()
        with self.assertRaises(TypeError):
            s1.to_dict(5)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestBaseModelFromDict(unittest.TestCase):
    def testRecreate(self):
        s1 = State()
        s1_dict = s1.to_dict()

        with patch('models.storage.new') as m:
            s2 = State(**s1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(s1_dict, s2.to_dict())
        self.assertIsNot(s1, s2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "State",
                     'name': "Lagos",
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        s1 = State(**cust_dict)
        self.assertEqual(s1.to_dict(), cust_dict)
        self.assertEqual(type(s1.updated_at), datetime.datetime)
        self.assertGreater(s1.updated_at, s1.created_at)
        self.assertEqual(s1.name, "Lagos")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        s1 = State("test", "kwargs", unused_id, unused_date)
        self.assertEqual(s1.to_dict(),
                         {'__class__': 'State',
                          'updated_at': '{}'.format(s1.updated_at.isoformat()),
                          'created_at': '{}'.format(s1.created_at.isoformat()),
                          'id': s1.id})
        self.assertNotEqual(s1.id, unused_id)
        self.assertNotEqual(s1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        s1 = BaseModel()
        s1_dict = s1.to_dict()

        s2 = BaseModel("test", str(uuid.uuid4()),
                       datetime.datetime.now(), **s1_dict)
        self.assertEqual(s1_dict, s2.to_dict())
        self.assertEqual(s1.__dict__, s2.__dict__)
        self.assertIsNot(s1, s2)
