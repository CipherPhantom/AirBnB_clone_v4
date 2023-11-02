#!/usr/bin/python3
"""
Unittest for console

This module contains the required tests for the specified file
"""
import unittest
import os
import MySQLdb
from io import StringIO
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models import storage
from unittest.mock import patch
from console import HBNBCommand


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "For FileStorage")
class TestCreateMethodFileStorage(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        FileStorage._FileStorage__objects = {}
        if os.path.exists("file.json"):
            os.remove("file.json")

    def setUp(self):
        FileStorage._FileStorage__objects = {}

    def testCreateState(self):
        cmd = 'create State name="Arizona"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "State")
            self.assertEqual(obj.name, "Arizona")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreatePlace(self):
        cmd = 'create Place city_id="0001" user_id="0001" \
               name="My_little_house" number_rooms=4 number_bathrooms=2 \
               max_guest=10 price_by_night=300 latitude=37.773972 \
               longitude=-122.431297'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "Place")
            self.assertEqual(obj.max_guest, 10)
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateCity(self):
        cmd = 'create City state_id="95a5abab-aa65-4861-9bc6-1da4a36069aa" \
               name="San_Francisco"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "City")
            self.assertEqual(obj.name, "San Francisco")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateUser(self):
        cmd = 'create User email="gui@hbtn.io" password="guipwd" \
               first_name="Guillaume" last_name="Snow"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "User")
            self.assertEqual(obj.password, "guipwd")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateReview(self):
        cmd = 'create Review place_id="ed72aa02-3286-4891-acbc-9d9fc80a1103" \
               user_id="d93638d9-8233-4124-8f4e-17786592908b" \
               text="Amazing_place,_huge_kitchen"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "Review")
            self.assertEqual(obj.text, "Amazing place, huge kitchen")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateAmenity(self):
        cmd = 'create Amenity name="Wifi"'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "Amenity")
            self.assertEqual(obj.name, "Wifi")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))

    def testCreateBaseModel(self):
        cmd = 'create BaseModel'
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj = list(storage.all().values())[0]
            self.assertEqual(type(obj).__name__, "BaseModel")
            self.assertEqual(mck.getvalue(), "{}\n".format(obj.id))


@unittest.skipUnless(os.getenv("HBNB_TYPE_STORAGE") == "db", "For Database")
class TestForCreateMethodDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        args = [os.getenv("HBNB_MYSQL_HOST"), os.getenv("HBNB_MYSQL_USER"),
                os.getenv("HBNB_MYSQL_PWD"), os.getenv("HBNB_MYSQL_DB")]

        cls._conn = MySQLdb.connect(host=args[0], port=3306, user=args[1],
                                    passwd=args[2], db=args[3], charset="utf8")

        # Dictionary to enable reuse of created objects(rows)
        cls._aIds = {'City': None, 'User': None, 'Place': None, 'State': None,
                     'Amenity': None, 'Review': None}

    @classmethod
    def tearDownClass(cls):
        cls._conn.close()

    def setUp(self):
        self.cur = self._conn.cursor()

    def tearDown(self):
        self.cur.close()

    def createRow(self, model, args):

        tmplts = {'State': 'create State name="Arizona"',
                  'User': 'create User email="gui@hbtn.io" password="guipwd" \
                           first_name="Guillaume" last_name="Snow"',
                  'Place': 'create Place city_id="{}" user_id="{}" \
                            name="My_little_house" number_rooms=4 \
                            number_bathrooms=2 \
                            max_guest=10 price_by_night=300 latitude=37.773 \
                            longitude=-122.431297',
                  'City': 'create City state_id="{}" \
                           name="San_Francisco"',
                  'Amenity': 'create Amenity name="Wifi"',
                  'Review': 'create Review place_id="{}" \
                             user_id="{}" \
                             text="Amazing_place,_huge_kitchen"'
                  }
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(tmplts[model].format(*args))
            self._conn.commit()

            obj_id = mck.getvalue()[:-1]
            self._aIds[model] = obj_id
        return (obj_id)

    def testCreateState(self):
        model = "State"
        q_str = 'SELECT * FROM states'

        cmd = f'create {model} name="Arizona"'

        self.cur.execute(q_str)
        i_count = self.cur.rowcount
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj_id = mck.getvalue()[:-1]
            self._aIds[model] = self._aIds[model] or obj_id

            obj = storage.all()[f'{model}.{obj_id}']
            self.assertEqual(obj.name, "Arizona")

            self._conn.commit()
            self.cur.execute(q_str)
            self.assertTrue(self.cur.rowcount - i_count == 1)

    def testCreateUser(self):
        model = "User"
        q_str = 'SELECT * FROM users'

        cmd = f'create {model} email="gui@hbtn.io" password="guipwd" \
                first_name="Guillaume" last_name="Snow"'

        self.cur.execute(q_str)
        i_count = self.cur.rowcount
        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj_id = mck.getvalue()[:-1]
            self._aIds[model] = self._aIds[model] or obj_id

            obj = storage.all()[f'{model}.{obj_id}']
            self.assertEqual(obj.password, "guipwd")

            self._conn.commit()
            self.cur.execute(q_str)
            self.assertTrue(self.cur.rowcount - i_count == 1)

    def testCreateCity(self):
        model = "City"
        q_str = 'SELECT * FROM cities'

        s_id = self._aIds["State"] or self.createRow("State", [])
        cmd = f'create {model} state_id="{s_id}" name="San_Francisco"'

        self.cur.execute(q_str)
        i_count = self.cur.rowcount

        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj_id = mck.getvalue()[:-1]
            obj = storage.all()[f'{model}.{obj_id}']
            self.assertEqual(obj.name, "San Francisco")

            self._conn.commit()
            self.cur.execute(q_str)
            self.assertTrue(self.cur.rowcount - i_count == 1)

    def testCreatePlace(self):
        model = "Place"
        q_str = 'SELECT * FROM places'

        s_id = self._aIds["State"] or self.createRow("State", [])
        c_id = self._aIds["City"] or self.createRow("City", [s_id])
        u_id = self._aIds["User"] or self.createRow("User", [])

        cmd = f'create {model} city_id="{c_id}" user_id="{u_id}" \
                name="My_little_house" number_rooms=4 number_bathrooms=2 \
                max_guest=10 price_by_night=300 latitude=37.773972 \
                longitude=-122.431297'

        self.cur.execute(q_str)
        i_count = self.cur.rowcount

        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj_id = mck.getvalue()[:-1]
            obj = storage.all()[f'{model}.{obj_id}']
            self.assertEqual(obj.number_rooms, 4)

            self._conn.commit()
            self.cur.execute(q_str)
            self.assertTrue(self.cur.rowcount - i_count == 1)

    def testCreateReview(self):
        model = "Review"
        q_str = 'SELECT * FROM reviews'

        u_id = self._aIds["User"] or self.createRow("User", [])
        s_id = self._aIds["State"] or self.createRow("State", [])
        c_id = self._aIds["City"] or self.createRow("City", [s_id])
        p_id = self._aIds["Place"] or self.createRow("Place", [c_id, u_id])

        cmd = f'create {model} place_id="{p_id}" \
                user_id="{u_id}" \
                text="Amazing_place,_huge_kitchen"'

        self.cur.execute(q_str)
        i_count = self.cur.rowcount

        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj_id = mck.getvalue()[:-1]
            obj = storage.all()[f'{model}.{obj_id}']
            self.assertEqual(obj.text, "Amazing place, huge kitchen")

            self._conn.commit()
            self.cur.execute(q_str)
            self.assertTrue(self.cur.rowcount - i_count == 1)

    def testCreateAmenity(self):
        model = "Amenity"
        q_str = 'SELECT * FROM amenities'

        cmd = 'create Amenity name="Wifi"'

        self.cur.execute(q_str)
        i_count = self.cur.rowcount

        with patch('sys.stdout', new=StringIO()) as mck:
            HBNBCommand().onecmd(cmd)
            obj_id = mck.getvalue()[:-1]
            obj = storage.all()[f'{model}.{obj_id}']
            self.assertEqual(obj.name, "Wifi")

            self._conn.commit()
            self.cur.execute(q_str)
            self.assertTrue(self.cur.rowcount - i_count == 1)
