from app.tests.v1.test_config import APITestcase
from flask import json

class TestFetchOrderHistoryEndpoint(APITestcase):
    def login(self):
        response = self.test_client.post(
            'api/v1/auth/login',
            data=json.dumps(
                {
                    "username": "johndoe1",
                    "password": "johndoe@A1"
                }),
            content_type="application/json")

        self.access_token = json.loads(response.data)['access_token']


    def test_endpoint(self):
        self.login()

        response = self.test_client.get(
            '/api/v1/users/orders',
            headers={
                "Authorization": "Bearer " + self.access_token
            })

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Successfully fetched user order history!",
            "Unexpected response message!")