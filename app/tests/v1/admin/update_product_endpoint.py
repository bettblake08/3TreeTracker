from app.tests.v1.test_config import APITestCase
from flask import json


class TestPostNewProductEndpoint(APITestCase):
    running_tests = 0

    def setUp(self):
        if self.running_tests == 0:
            self.admin_login()

        self.running_tests += 1

        import pdb; pdb.set_trace()

    def tearDown(self):
        self.running_tests -= 1 

        if self.running_tests == 0:
            self.admin_logout()

        import pdb; pdb.set_trace()

    def post_new_product(self, data, product_id):
        return self.test_client.put(
            '/api/v1/admin/product/' + product_id,
            data=data,
            content_type='application/json'
        )

    def test_using_no_title_field(self):
        response = self.post_new_product(
            product_id=1,
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
            product_id=1,
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
            product_id=1,
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
            product_id=1,
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
            product_id=1,
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
            product_id=1,
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
            product_id=1,
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

    def test_using_invalid_id(self):

        response = self.post_new_product(
            product_id="ro",
            data=json.dumps(
                {
                    "pro__title": "This is a new product",
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

    def test_using_unexisting_product_id(self):

        response = self.post_new_product(
            product_id=60,
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
            404,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Product not found!",
            "Unexpected response message!")

    def test_using_valid_data(self):

        response = self.post_new_product(
            product_id=1,
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
