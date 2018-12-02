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

        cls.response = None
        
        cls.test_client = cls.app.test_client()

    @classmethod
    def admin_login(cls):
        cls.test_client.post(
            'api/v1/admin/login',
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }),
            content_type="application/json")

    @classmethod
    def admin_logout(cls):
        cls.test_client.get('/api/v1/admin/logout')

    @classmethod
    def tearDownClass(cls):
        DATABASE.session.session_factory.close_all()
        DATABASE.drop_all()

    def check_status_code(self, response, status_code):
        self.assertEqual(
            response.status_code,
            status_code,
            "Unexpected status code!"
        )

    def check_response_message(self, response, expected_message):
        data = json.loads(response.data)

        self.assertEqual(
            data["message"],
            expected_message,
            "Unexpected response message!"
        )

class AdminAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        super().admin_login()

    @classmethod
    def tearDownClass(cls):
        super().admin_logout()
        super().tearDownClass()
