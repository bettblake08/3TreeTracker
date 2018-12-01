from app.tests.v1.test_config import APITestCase

class TestSetReactionEndpoint(APITestCase):

    def set_reaction(self, data):
        return self.test_client.get(
            "api/v1/productReaction/{}/{}".format(data["pid"], data["rid"])
        )

    def test_using_invalid_product_id(self):

        response = self.set_reaction(
            {
                "pid": "ro",
                "rid": 1
            }
        ) 

        self.check_status_code(response, 400)
        self.check_response_message(response, "Invalid request!")


    def test_using_unexisting_product_id(self):

        response = self.set_reaction(
            {
                "pid": 999,
                "rid": 1
            }
        )

        self.check_status_code(response, 404)
        self.check_response_message(response, "Product does not exist!")


    def test_using_invalid_reaction_id(self):

        response = self.set_reaction(
            {
                "pid": 1,
                "rid": "ro"
            }
        )

        self.check_status_code(response, 400)
        self.check_response_message(response, "Invalid request!")

    def test_using_incorrect_reaction_id(self):

        response = self.set_reaction(
            {
                "pid": 1,
                "rid": 6
            }
        )

        self.check_status_code(response, 400)
        self.check_response_message(response, "Invalid reaction id!")

    def test_using_valid_data(self):

        response = self.set_reaction(
            {
                "pid": 1,
                "rid": 1
            }
        )

        self.check_status_code(response, 200)
        self.check_response_message(
            response,
            "You have successfully set a reaction to the product!"
            )
