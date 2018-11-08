from app.tests.v1.test_config import APITestcase
from flask import json

class TestTokenRefreshEndpoint(APITestcase):
    def login(self):
        response = self.test_client.post('api/v1/auth/login',
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }),
            content_type="application/json")


        self.refresh_token = json.loads(response.data)['refresh_token']

    def test_fetch_refreshed_token(self):
        self.login()

        response = self.test_client.get('/api/v1/token/refresh',
            headers={
                "Authorization": "Bearer " + self.refresh_token
            })

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            201,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Refresh successful!",
            "Unexpected response message!")

        self.assertNotEqual(
            data['access_token'],
            "",
            "Access token is empty!")
