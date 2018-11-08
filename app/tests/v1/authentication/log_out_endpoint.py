from app.tests.v1.test_config import APITestcase
from flask import json
import pytest

class TestLogOutEndpoint(APITestcase):
    def login(self):
        response = self.test_client.post('api/v1/auth/login',
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }),
            content_type="application/json")

        self.access_token = json.loads(response.data)['access_token']

    @pytest.mark.run(order=1)
    def test_log_out(self):
        self.login()

        response_1 = self.test_client.get('/api/v1/auth/logout',
            headers={
                "Authorization": "Bearer " + self.access_token
            })

        response_2 = self.test_client.get(
            '/api/v1/order/1',
            headers={
                "Authorization": "Bearer " + self.access_token
            }
        )

        data_1 = json.loads(response_1.data)
        data_2 = json.loads(response_2.data)

        self.assertEqual(
            response_1.status_code,
            200,
            "Unexpected response status!")

        self.assertEqual(
            data_1['message'],
            "Access token has been revoked!",
            "Unexpected response message!")

        self.assertEqual(
            response_2.status_code,
            401,
            "Unexpected response status!")

        self.assertEqual(
            data_2['msg'],
            "Token has been revoked",
            "Unexpected response message!")
