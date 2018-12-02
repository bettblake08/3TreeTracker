import json

from app.tests.v1.test_config import AdminAPITestCase

class TestSoftDeleteRepoFileEndpoint(AdminAPITestCase):

    def delete(self, file_id):

        return self.test_client.get(
            "api/v1/admin/repoFile/{}".format(file_id)
        )

    def test_using_invalid_file_id(self):

        response = self.delete("ro")

        self.check_status_code(response, 400)
        self.check_response_message(response, "Invalid file id!")

    def test_using_unexisting_file_id(self):

        response = self.delete(999)

        self.check_status_code(response, 404)
        self.check_response_message(
            response,
            "Repo file does not exist!"
        )

    def test_using_used_file_id(self):

        response = self.delete(1)

        self.check_status_code(response, 403)
        self.check_response_message(
            response,
            "Repo file is currently being used!"
        )

    def test_using_valid_file_id(self):

        response = self.delete(2)

        self.check_status_code(response, 200)
        self.check_response_message(
            response,
            "You have successfully deleted the repo file!"
        )
