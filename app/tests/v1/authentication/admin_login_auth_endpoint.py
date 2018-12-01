from app.tests.v1.test_config import APITestCase
from flask import json

class TestLoginAuthEndpoint(APITestCase):
    def auth_user(self, data):
        return self.test_client.post(
            '/api/v1/admin/login',
            data=data,
            content_type='application/json'
            )

    def test_using_no_username_field(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "userna": "jamesblack",
                    "password": "testPASS.A1"
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")


    def test_using_no_password_field(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "jamesblack",
                    "passwd": "testPASS.A1"
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")     

    def test_using_invalid_password_value(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "m21c07ss"
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Password is invalid!",
            "Unexpected response message!"
            )


    def test_using_username_that_doesnt_exist(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "jamesblack0807",
                    "password": "testPASS.A1"
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 
            404,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "User jamesblack0807 does not exist!",
            "Unexpected response message!")


    def test_using_email_that_doesnt_exist(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "bettblake07@hotmail.com",
                    "password": "testPASS.A1"
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            404,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "User bettblake07@hotmail.com does not exist!",
            "Unexpected response message!")

    def test_using_admin_user_username(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }
            ))

        url_response = self.test_client.get("/api/v1/admin/getProducts/0")

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Logged in as johndoe2!",
            "Unexpected response message!")

        self.assertEqual(
            url_response.status_code,
            200,
            "User has not been connected!"
        )

    def test_using_admin_email_as_username(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe2@hotmail.com",
                    "password": "johndoe@A2"
                }
            ))

        self.assertEqual(
            response.status_code, 
            404,
            "Unexpected response status!")
