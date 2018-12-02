from flask import json

from app.tests.v1.test_config import AdminAPITestCase
from app.tests.v1.test_data import ADMIN_USER


class TestPostNewAdminUserEndpoint(AdminAPITestCase):
    
    def post_new_user(self, data):
        return self.test_client.post(
            '/api/v1/admin/user/none',
            data=data,
            content_type='application/json'
        )

    def test_using_no_username_field(self):

        response = self.post_new_user(
            data=json.dumps({
                "user": ADMIN_USER.get("username"),
                "password": ADMIN_USER.get("password")
            })
        )

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")
        
        self.assertEqual(
            data['message']['username'],
            "The username field is required!",
            "Unexpected response message!")

    def test_using_no_password_field(self):

        response = self.post_new_user(
            data=json.dumps({
                "username": ADMIN_USER.get("username"),
                "pass": ADMIN_USER.get("password")
            })
        )

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

        self.assertEqual(
            data['message']['password'],
            "The password field is required!",
            "Unexpected response message!")

    def test_using_no_username(self):

        response = self.post_new_user(
            data=json.dumps({
                "username": "",
                "password": ADMIN_USER.get("password")
            })
        )

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "The username value is required!",
            "Unexpected response message!")

    def test_using_no_password(self):

        response = self.post_new_user(
            data=json.dumps({
                "username": ADMIN_USER.get("username"),
                "password": ""
            })
        )

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "The password value is required!",
            "Unexpected response message!")

    def test_using_invalid_password(self):

        response = self.post_new_user(
            data=json.dumps({
                "username": ADMIN_USER.get("username"),
                "password": ADMIN_USER.get("invalid_password")
            })
        )

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Invalid password!",
            "Unexpected response message!")

    def test_using_valid_data(self):

        response = self.post_new_user(
            data=json.dumps({
                "username": ADMIN_USER.get("username"),
                "password": ADMIN_USER.get("password")
            })
            )

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            201,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "You have successfully created an admin user account!",
            "Unexpected response message!")
