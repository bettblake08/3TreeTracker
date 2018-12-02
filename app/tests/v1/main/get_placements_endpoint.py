import json

from app.tests.v1.test_config import APITestCase


class TestGetPlacementsEndpoint(APITestCase):

    def get_placement(self, name):

        return self.test_client.get(
            "api/v1/getPlacements/{}".format(name)
        )

    def test_using_unexisting_username(self):

        response = self.get_placement("james jordan")

        self.check_status_code(response, 200)
        self.check_response_message(
            response,
            "You have successfully retrieved the list of placements!"
        )

        data = json.loads(response.data)

        self.assertEqual(
            len(data["content"]),
            0,
            "Unexpected content length!"
        )

    def test_using_valid_data(self):
        response = self.get_placement("john doe")

        self.check_status_code(response, 200)
        self.check_response_message(
            response,
            "You have successfully retrieved the list of placements!"
        )
        