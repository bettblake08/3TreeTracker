""" This module hosts all test configurations for running test on api """
import unittest
from app import create_app
from db import db
from app.database.factory import generate_test_data




class APITestCase(unittest.TestCase):
    """ This class is the base test class """
    @classmethod
    def setUpClass(self):
        self.app = create_app("TEST")
        self.app.app_context().push()
        db.create_all()
        generate_test_data()
        self.test_client = self.app.test_client()

    @classmethod
    def tearDownClass(self):
        db.drop_all()
