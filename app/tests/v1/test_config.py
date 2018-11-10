""" This module hosts all test configurations for running test on api """
import unittest
from app import create_app
from db import db
from app.database.factory import generate_test_data
from app.database import create_test_database
import json
class APITestCase(unittest.TestCase):
    """ This class is the base test class """
    @classmethod
    def setUpClass(cls):
        create_test_database()

        cls.app = create_app("TEST")
        cls.app.app_context().push()

        db.create_all()
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
        db.session.session_factory.close_all()
        db.drop_all()
