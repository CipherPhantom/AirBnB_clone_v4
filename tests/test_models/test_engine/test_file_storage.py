#!/usr/bin/python3
"""
Unittest for models.engine.file_storage([..])

This module contains the required tests for the specified module
"""
import unittest
import datetime
from models.base_model import BaseModel
from models import storage
import models.engine.file_storage
from models.engine.file_storage import FileStorage
from unittest.mock import patch, mock_open
import os
import json
from models.state import State


def fake_new_method(obj):
    return


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
def setUpModule():
    FileStorage._FileStorage__objects = {}
    if os.path.exists("file.json"):
        os.remove("file.json")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestAllFileStorageDocstrings(unittest.TestCase):
    def testModuleDocstring(self):
        self.assertGreater(len(models.engine.file_storage.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.engine.file_storage, "FileStorage"))
        self.assertGreater(len(FileStorage.__doc__), 1)

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


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestFileStorageClass(unittest.TestCase):
    def test_PrivateAttributeAccess(self):
        with self.assertRaises(AttributeError):
            print(storage.__file_path)
        with self.assertRaises(AttributeError):
            print(storage.__objects)

    def test_PrivateAttributesType(self):
        self.assertEqual(type(FileStorage._FileStorage__file_path), str)
        self.assertEqual(type(FileStorage._FileStorage__objects), dict)
        self.assertEqual(FileStorage._FileStorage__file_path, "file.json")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestAllMethod(unittest.TestCase):
    def testReturnValueForAllMethod(self):
        self.assertEqual(type(storage.all()), dict)
        self.assertEqual(storage.all(), FileStorage._FileStorage__objects)

    def testReturnValueContentForAllMethod(self):
        FileStorage._FileStorage__objects = {}
        with patch('models.storage.new', fake_new_method):
            b1 = BaseModel()
            b2 = BaseModel()
        k1 = '{}.{}'.format(type(b1).__name__, b1.id)
        k2 = '{}.{}'.format(type(b2).__name__, b2.id)
        storage.new(b1)
        storage.new(b2)
        all_dict = storage.all()
        self.assertIs(all_dict[k1], b1)
        self.assertIs(all_dict[k2], b2)
        FileStorage._FileStorage__objects = {}


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestReloadMethod(unittest.TestCase):
    def testReloadForAbsentFile(self):
        storage.reload()
        self.assertEqual(storage.all(), {})

    def testReloadWithEmptyFile(self):
        fname = "file.json"
        filecontent = ""
        with patch('models.engine.file_storage.open',
                   mock_open(read_data=filecontent)) as mock_file:
            self.assertRaises(json.decoder.JSONDecodeError,  storage.reload)
            mock_file.assert_called_once_with(fname, encoding='utf-8')
            self.assertEqual(storage.all(), {})

    def testReloadMethodWithValidFile(self):
        with patch('models.storage.new', fake_new_method):
            b1 = BaseModel()
            key = '{}.{}'.format(type(b1).__name__, b1.id)
            f_dict = {key: b1.to_dict()}
            fname = "file.json"
            fcontent = json.dumps(f_dict)
            os.mknod('file.json')
        with patch('models.engine.file_storage.open',
                   mock_open(read_data=fcontent)) as mock_file:
            storage.reload()

            #  mock_file.assert_called_once_with(fname, 'r',
            self.assertEqual(storage.all()[key].to_dict(), b1.to_dict())
        FileStorage._FileStorage__objects = {}

    def testReloadMethodWithArg(self):
        with self.assertRaises(TypeError):
            storage.reload("arg")


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestNewMethod(unittest.TestCase):
    def testNewWithNoArg(self):
        with self.assertRaises(TypeError):
            storage.new()

    def testNewWithArg(self):
        FileStorage._FileStorage__objects = {}
        with patch('models.storage.new', fake_new_method):
            b1 = BaseModel()
            key1 = '{}.{}'.format(type(b1).__name__, b1.id)
            b2 = BaseModel()
            key2 = '{}.{}'.format(type(b2).__name__, b2.id)

        with self.assertRaises(TypeError):
            storage.new(b1, b2)
        storage.new(b1)
        storage.new(b2)
        self.assertEqual(storage.all()[key1], b1)
        self.assertEqual(storage.all()[key2], b2)
        FileStorage._FileStorage__objects = {}


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestSaveMethod(unittest.TestCase):
    def testSaveMethodWithArg(self):
        with self.assertRaises(TypeError):
            storage.save({})

    def testSaveEmptyObjectsDict(self):
        FileStorage._FileStorage__objects = {}
        fname = "file.json"
        fcontent = json.dumps({})
        with patch('models.engine.file_storage.open',
                   mock_open()) as mock_file:
            storage.save()
            mock_file.assert_called_once_with(fname, 'w',
                                              encoding='utf-8')
        FileStorage._FileStorage__objects = {}

    def testSaveMethodWithValidFile(self):
        FileStorage._FileStorage__objects = {}
        b1 = BaseModel()
        b2 = BaseModel()
        key1 = '{}.{}'.format(type(b1).__name__, b1.id)
        key2 = '{}.{}'.format(type(b2).__name__, b2.id)
        f_dict = {key1: b1.to_dict(), key2: b2.to_dict()}
        fname = "file.json"
        fcontent = json.dumps(f_dict)
        with patch('models.engine.file_storage.open',
                   mock_open()) as mock_file:
            storage.save()
            mock_file.assert_called_once_with(fname, 'w',
                                              encoding='utf-8')
        FileStorage._FileStorage__objects = {}


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestCountMethod(unittest.TestCase):
    def testCountMethodWithNoArg(self):
        self.assertEqual(storage.count(), len(storage.all()))

    def testCountMethodWithClass(self):
        self.assertEqual(storage.count(State), len(storage.all(State)))


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
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
