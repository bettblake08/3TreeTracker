""" This module hosts all test configurations for running test on api """
import json
import unittest

from app import create_app
from app.database import create_database
from app.database.db import DATABASE
from app.database.factory import generate_test_data


class APITestCase(unittest.TestCase):
    """ This class is the base test class """
    @classmethod
    def setUpClass(cls):
        create_database("TEST")

        cls.app = create_app("TEST")
        cls.app.app_context().push()

        DATABASE.create_all()
        generate_test_data()
        
        cls.test_client = cls.app.test_client()

    def admin_login(self):
        self.test_client.post(
            'api/v1/admin/login',
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }),
            content_type="application/json")

    def admin_logout(self):
        self.test_client.get('/api/v1/admin/logout')

    @classmethod
    def tearDownClass(cls):
        DATABASE.session.session_factory.close_all()
        DATABASE.drop_all()
