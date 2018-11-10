from app.tests.v1.test_config import APITestCase
from flask import json


class TestPostNewProductEndpoint(APITestCase):
    def setUp(self):
        self.admin_login()

    def tearDown(self):
        self.admin_logout()

    def post_new_product(self, data):
        return self.test_client.post(
            '/api/v1/admin/product/0',
            data=data,
            content_type='application/json'
        )

    def test_using_no_title_field(self):
        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__tit": "This is a new product",
                    "pro__body": "<p>This is a test body</p>",
                    "pro__summary": "This is a summary",
                    "pro__image": 1,
                    "pro__tags": json.dumps([1])
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

    def test_using_no_body_field(self):
        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
                    "pro__": "<p>This is a test body</p>",
                    "pro__summary": "This is a summary",
                    "pro__image": 1,
                    "pro__tags": json.dumps([1])
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")


    def test_using_no_summary_field(self):
        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
                    "pro__body": "<p>This is a test body</p>",
                    "pro__summy": "This is a summary",
                    "pro__image": 1,
                    "pro__tags": json.dumps([1])
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")


    def test_using_no_image_id_field(self):
        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
                    "pro__body": "<p>This is a test body</p>",
                    "pro__summary": "This is a summary",
                    "pro__ime": 1,
                    "pro__tags": json.dumps([1])
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")



    def test_using_no_tags_field(self):
        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
                    "pro__body": "<p>This is a test body</p>",
                    "pro__summary": "This is a summary",
                    "pro__image": 1,
                    "pro__ta": json.dumps([1])
                }
            ))

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

    def test_using_unexisting_image_id(self):

        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
                    "pro__body": "<p>This is a test body</p>",
                    "pro__summary": "This is a summary",
                    "pro__image": 999,
                    "pro__tags": json.dumps([1])
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            404,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Image not found!",
            "Unexpected response message!")

    def test_using_invalid_tag_array(self):

        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
                    "pro__body": "<p>This is a test body</p>",
                    "pro__summary": "This is a summary",
                    "pro__image": 1,
                    "pro__tags": ","
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            400,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Invalid tag list!",
            "Unexpected response message!")

    def test_using_valid_data(self):

        response = self.post_new_product(
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
                    "pro__body": "<p>This is a test body</p>",
                    "pro__summary": "This is a summary",
                    "pro__image": 1,
                    "pro__tags": json.dumps([1])
                }
            ))

        data = json.loads(response.data)

        self.assertEqual(
            response.status_code,
            201,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "You have successfully posted a new product!",
            "Unexpected response message!")
