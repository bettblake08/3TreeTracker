import json

from app.tests.v1.test_config import AdminAPITestCase


class TestRetrieveRepoContentByFolderEndpoint(AdminAPITestCase):

    def retrieve_content(self, folder_id):
        return self.test_client.get(
            "api/v1/admin/retrieveRepoContentByFolder/{}".format(folder_id)
        )

    def test_using_invalid_folder_id(self):

        response = self.retrieve_content("base")

        self.check_status_code(response, 400)
        self.check_response_message(
            response,
            "Invalid folder id!"
        )

    def test_using_unexisting_folder_id(self):

        response = self.retrieve_content(999)

        self.check_status_code(response, 404)
        self.check_response_message(
            response,
            "Repo folder does not exist!"
        )

    def test_using_root_folder_id(self):
        response = self.retrieve_content("root")

        self.check_status_code(response, 200)
        self.check_response_message(
            response,
            "You have successfully retrieved the repo folder content!"
        )
    
    def test_using_valid_data(self):

        response = self.retrieve_content(1)

        self.check_status_code(response, 200)
        self.check_response_message(
            response,
            "You have successfully retrieved the repo folder content!"
        )
