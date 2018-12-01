import json

from app.tests.v1.test_config import APITestCase


class TestGetPlacementsEndpoint(APITestCase):

    def get_placement(self, name):

        return self.test_client.get(
            "api/v1/getPlacements/{}".format(name)
        )

    def test_using_unexisting_username(self):

        response = self.get_placement("james jordan")

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected status code!"
        )

        self.assertEqual(
            data["message"],
            "You have successfully retrieved the list of placements!",
            "Unexpected response message!"
        )

        self.assertEqual(
            len(data["content"]),
            0,
            "Unexpected content length!"
        )

    def test_using_valid_data(self):
        response = self.get_placement("john doe")

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            200,
            "Unexpected status code!"
        )

        self.assertEqual(
            data['message'],
            "You have successfully retrieved the list of placements!",
            "Unexpected response message!"
        )
