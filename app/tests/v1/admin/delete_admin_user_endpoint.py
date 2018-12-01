from flask import json

from app.tests.v1.test_config import ADMINAPITestCase
from app.tests.v1.test_data import ADMIN_USER


class TestDeleteAdminUserEndpoint(ADMINAPITestCase):
    def delete_user(self, data):
        return self.test_client.delete(
            '/api/v1/admin/user/{}'.format(data)
        )

    def test_using_unexisting_username(self):
        response = self.delete_user("none")

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            404,
            "Unexpected status code!"
        )

        self.assertEqual(
            data['message'],
            "Admin user does not exist!",
            "Unexpected response message!"
        )


    def test_using_valid_data(self):
        response = self.delete_user("johndoe2")

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected status code!"
        )

        self.assertEqual(
            data['message'],
            "You have successfully deleted the admin account!",
            "Unexpected response message!"
        )
    
