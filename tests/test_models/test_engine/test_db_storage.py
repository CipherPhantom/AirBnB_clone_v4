#!/usr/bin/python3
"""
Unittest for models.engine.db_storage([..])

This module contains the required tests for the specified module
"""
import unittest
import datetime
from models.base_model import BaseModel
from models.base_model import Base
from models.state import State
from models import storage
import models.engine.db_storage
from models.engine.db_storage import DBStorage
from unittest.mock import patch, mock_open
import os
import json


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For db Storage")
class TestAllDBStorageDocstrings(unittest.TestCase):
    def testModuleDocstring(self):
        self.assertGreater(len(models.engine.db_storage.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.engine.db_storage, "DBStorage"))
        self.assertGreater(len(DBStorage.__doc__), 1)

    def testAllFnDocstring(self):
        self.assertTrue(hasattr(storage, "all"))
        self.assertGreater(len(storage.all.__doc__), 1)

    def testNewFnDocstring(self):
        self.assertTrue(hasattr(storage, "new"))
        self.assertGreater(len(storage.new.__doc__), 1)

    def testSaveFnDocstring(self):
        self.assertTrue(hasattr(storage, "save"))
        self.assertGreater(len(storage.save.__doc__), 1)

    def testReloadFnDocstring(self):
        self.assertTrue(hasattr(storage, "reload"))
        self.assertGreater(len(storage.__doc__), 1)


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For db Storage")
class TestFileStorageClass(unittest.TestCase):
    def test_PrivateAttributeAccess(self):
        with self.assertRaises(AttributeError):
            print(storage.__engine)
        with self.assertRaises(AttributeError):
            print(storage.__session)


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For db Storage")
class TestAllMethod(unittest.TestCase):
    def testReturnValueForAllMethod(self):
        self.assertEqual(type(storage.all(State)), dict)

    def testReturnValueContentForAllMethod(self):
        sess = storage._DBStorage__session
        s1 = State(name="Los Angeles")
        k1 = '{}.{}'.format(type(s1).__name__, s1.id)
        sess.add(s1)
        sess.commit()

        all_dict = storage.all(State)

        self.assertIs(all_dict[k1], s1)


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestReloadMethod(unittest.TestCase):
    def testReloadMethodFromEmptyDb(self):
        storage.reload()
        state_table = Base.metadata.tables['states']

        self.assertIs(state_table, State.__table__)

    def testReloadMethodWithArg(self):
        with self.assertRaises(TypeError):
            storage.reload("arg")


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestNewMethod(unittest.TestCase):
    def testNewWithNoArg(self):
        with self.assertRaises(TypeError):
            storage.new()

    def testNewWithArg(self):
        sess = storage._DBStorage__session
        s1 = State(name="Los Angeles")
        s2 = State(name="Florid")
        key1 = '{}.{}'.format(type(s1).__name__, s1.id)

        with self.assertRaises(TypeError):
            storage.new(s1, s2)
        storage.new(s2)
        new_st = sess.query(State).filter_by(name="Florid").first()
        self.assertIs(s2, new_st)


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestSaveMethod(unittest.TestCase):
    def testSaveMethodWithArg(self):
        with self.assertRaises(TypeError):
            storage.save({})

    def testSaveMethodWithDB(self):
        sess = storage._DBStorage__session
        s1 = State(name="Lagos")
        s2 = State(name="Nairobi")

        sess.add_all([s1, s2])

        storage.save()
        new_s1 = sess.query(State).filter_by(name="Lagos").first()
        new_s2 = sess.query(State).filter_by(name="Nairobi").first()

        self.assertIs(s1, new_s1)
        self.assertIs(s2, new_s2)


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For db Storage")
class TestGetMethod(unittest.TestCase):

    def testGetMethodWithDB(self):
        s1 = State(name="Lagos")
        s2 = State(name="Nairobi")

        storage.new(s1)
        storage.save()
        storage.new(s2)
        storage.save()
        new_s1 = storage.get(State, s1.id)
        new_s2 = storage.get(State, s2.id)

        self.assertIs(s1, new_s1)
        self.assertIs(s2, new_s2)

    def testGetMethodWithNotPresentId(self):
        self.assertIsNone(storage.get(State, "NotId"))


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For db Storage")
class TestCountMethod(unittest.TestCase):

    def testCountMethodWithNoArg(self):
        self.assertEqual(storage.count(), len(storage.all()))

    def testCountMethodWithClass(self):
        self.assertEqual(storage.count(State), len(storage.all(State)))
