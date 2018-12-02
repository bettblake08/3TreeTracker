import json

from app.tests.v1.test_config import APITestCase

class TestGetAllProductsEndpoint(APITestCase):

    def get_products(self, offset):
        return self.test_client.get(
            "api/v1/getProducts/{}".format(offset)
        )

    def test_using_invalid_offset(self):
        response = self.get_products("ro")

        self.check_status_code(response, 400)
        self.check_response_message(response, "Invalid offset!")

    def test_using_incorrect_offset(self):
        response = self.get_products(999)

        self.check_status_code(response, 404)
        self.check_response_message(
            response,
            "There are no more products to list from given offset!"
        )

    def test_using_valid_offset(self):

        response = self.get_products(0)

        self.check_status_code(response, 200)
        self.check_response_message(
            response,
            "You have successfully retrieved all the products!"
        )
