import json

from app.tests.v1.test_config import APITestCase

class TestGetAllProductsEndpoint(APITestCase):

    def get_products(self, offset):
        return self.test_client.get(
            "api/v1/getProducts/{}".format(offset)
        )

    def test_using_invalid_offset(self):

        response = self.get_products("ro")

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected status code!"
        )

        self.assertEqual(
            data['message'],
            "Invalid offset!",
            "Unexpected response message!"
        )


    def test_using_incorrect_offset(self):

        response = self.get_products(999)

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            404,
            "Unexpected status code!"
        )

        self.assertEqual(
            data['message'],
            "There are no more products to list from given offset!",
            "Unexpected response message!"
        )


    def test_using_valid_offset(self):

        response = self.get_products(0)

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected status code!"
        )

        self.assertEqual(
            data["message"],
            "You have successfully retrieved all the products!",
            "Unexpected response message!"
        )
