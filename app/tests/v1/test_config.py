""" This module hosts all test configurations for running test on api """
import unittest
from app import create_app
from db import db
from app.database.factory import generate_test_data

APP = create_app("TEST")


class TestModel(unittest.TestCase):
    """ This class is the base test class """

    def setUp(self):
        self.client = APP.test_client()
        db.create_all()
        generate_test_data()

    def tearDown(self):
        db.drop_all()
