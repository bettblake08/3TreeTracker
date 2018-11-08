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
            "Password is invalid. Please input a valid password!",
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
            "User jamesblack0807 doesn't exist!",
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
            "User bettblake07@hotmail.com doesn't exist!",
            "Unexpected response message!")


    def test_using_customer_username(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe1",
                    "password": "johndoe@A1"
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Logged in as johndoe1!",
            "Unexpected response message!")


    def test_using_customer_email_as_username(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe1@hotmail.com",
                    "password": "johndoe@A1"
                }
            ))
            

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected response status!")

        self.assertEqual(
            data['message'], 
            "Logged in as johndoe1!",
            "Unexpected response message!")


    def test_using_admin_user_username(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Logged in as johndoe2!",
            "Unexpected response message!")


    def test_using_admin_email_as_username(self):

        response = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe2@hotmail.com",
                    "password": "johndoe@A2"
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 
            200,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Logged in as johndoe2",
            "Unexpected response message!")


    def test_admin_access_using_customer(self):
        result = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe1",
                    "password": "johndoe@A1"
                }
            ))

        token = json.loads(result.data)['access_token']

        response = self.test_client.get(
            '/api/v1/order/1',
            headers={
                "Authorization": "Bearer " + token
            }
        )

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            403,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Only admin users have permission to access!",
            "Unexpected response message!")

    def test_admin_access_using_admin(self):
        result = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }
            ))

        token = json.loads(result.data)['access_token']

        response = self.test_client.get(
            '/api/v1/order/1',
            headers={
                "Authorization": "Bearer " + token
            }
        )

        self.assertNotEqual(
            response.status_code,
            403,
            "Unexpected response status!")

    def test_customer_access_using_admin(self):
        result = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }
            ))

        token = json.loads(result.data)['access_token']

        response = self.test_client.get(
            '/api/v1/users/orders',
            headers={
                "Authorization": "Bearer " + token
            }
        )

        self.assertEqual(
            response.status_code,
            403,
            "Unexpected response status!")

    def test_customer_access_using_customer(self):
        result = self.auth_user(
            data=json.dumps(
                {
                    "username": "johndoe1",
                    "password": "johndoe@A1"
                }
            ))

        token = json.loads(result.data)['access_token']

        response = self.test_client.get(
            '/api/v1/users/orders',
            headers={
                "Authorization": "Bearer " + token
            }
        )

        self.assertNotEqual(
            response.status_code,
            403,
            "Unexpected response status!")
