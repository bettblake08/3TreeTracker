from app.tests.v1.test_config import APITestCase
from flask import json
import pytest

class TestLogOutEndpoint(APITestCase):
    def login(self):
        self.test_client.post('api/v1/admin/login',
            data=json.dumps(
                {
                    "username": "johndoe2",
                    "password": "johndoe@A2"
                }),
            content_type="application/json")

    @pytest.mark.run(order=1)
    def test_log_out(self):
        self.login()

        response_1 = self.test_client.get('/api/v1/admin/logout')
        response_2 = self.test_client.get('/api/v1/admin/logout')

        data_1 = json.loads(response_1.data)

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
            302,
            "Unexpected response status!")
