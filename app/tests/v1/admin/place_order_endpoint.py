from app.tests.v1.test_config import APITestCase
from flask import json


class TestPlaceOrderEndpoint(APITestCase):
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

    def place_order(self, data):
        self.login()

        return self.test_client.post(
            '/api/v1/users/orders',
            data=data,
            content_type='application/json',
            headers={
                "Authorization": "Bearer " + self.access_token
            }
        )

    def test_using_unexisting_item_id(self):
        response = self.place_order(
            data=json.dumps(
                {
                    "items": json.dumps(
                        [{
                            "id": 101,
                            "quantity": 2
                        }, {
                            "id": 2,
                            "quantity": 2
                        }, {
                            "id": 3,
                            "quantity": 4
                        }]
                    )
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            404,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Item 101 doesn't exist!",
            "Unexpected response message!")

    def test_using_no_quantity_value_in_item(self):

        response = self.place_order(
            data=json.dumps(
                {
                    "items": json.dumps(
                        [{
                            "id": 1,
                            "q": 2
                        }, {
                            "id": 2,
                            "quantity": 2
                        }, {
                            "id": 3,
                            "quantity": 4
                        }]
                    )
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Item 1 doesn't have a quantity field!",
            "Unexpected response message!")

    def test_using_no_items_key(self):

        response = self.place_order(
            data=json.dumps(
                {
                    "item": json.dumps(
                        [{
                            "id": 1,
                            "quantity": 2
                        }, {
                            "id": 2,
                            "quantity": 2
                        }, {
                            "id": 3,
                            "quantity": 4
                        }]
                    )
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

    def test_using_valid_data(self):

        response = self.place_order(
            data=json.dumps({
                "items": json.dumps(
                    [{
                        "id": 1,
                        "quantity": 2
                    }, {
                        "id": 2,
                        "quantity": 2
                    }, {
                        "id": 3,
                        "quantity": 4
                    }]
                )
            }))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            201,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "You have successfully created a new order!",
            "Unexpected response message!")
