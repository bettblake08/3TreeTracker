from app.tests.v1.test_config import APITestCase

class TestGetProductEndpoint(APITestCase):

    def get_product(self, product_id):

        return self.test_client.get(
            "api/v1/getProduct/{}".format(product_id),
        )

    def test_using_invalid_product_id(self):

        response = self.get_product("ro")

        self.check_status_code(response, 400)
        self.check_response_message(response, "Invalid product Id!")
