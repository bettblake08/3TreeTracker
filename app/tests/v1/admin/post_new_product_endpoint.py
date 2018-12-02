from flask import json

from app.tests.v1.test_config import AdminAPITestCase
from app.tests.v1.test_data import PRODUCT


class TestPostNewProductEndpoint(AdminAPITestCase):

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
                    "pro__tit": PRODUCT.get("title"),
                    "pro__body": PRODUCT.get("body"),
                    "pro__summary": PRODUCT.get("summary"),
                    "pro__image": PRODUCT.get("image"),
                    "pro__tags": PRODUCT.get("tags")
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
                    "pro__title": PRODUCT.get("title"),
                    "pro__": PRODUCT.get("body"),
                    "pro__summary": PRODUCT.get("summary"),
                    "pro__image": PRODUCT.get("image"),
                    "pro__tags": PRODUCT.get("tags")
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
                    "pro__title": PRODUCT.get("title"),
                    "pro__body": PRODUCT.get("body"),
                    "pro__summy": PRODUCT.get("summary"),
                    "pro__image": PRODUCT.get("image"),
                    "pro__tags": PRODUCT.get("tags")
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
                    "pro__title": PRODUCT.get("title"),
                    "pro__body": PRODUCT.get("body"),
                    "pro__summary": PRODUCT.get("summary"),
                    "pro__ime": PRODUCT.get("image"),
                    "pro__tags": PRODUCT.get("tags")
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
                    "pro__title": PRODUCT.get("title"),
                    "pro__body": PRODUCT.get("body"),
                    "pro__summary": PRODUCT.get("summary"),
                    "pro__image": PRODUCT.get("image"),
                    "pro__ta": PRODUCT.get("tags")
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
                    "pro__title": PRODUCT.get("title"),
                    "pro__body": PRODUCT.get("body"),
                    "pro__summary": PRODUCT.get("summary"),
                    "pro__image": 999,
                    "pro__tags": PRODUCT.get("tags")
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
                    "pro__title": PRODUCT.get("title"),
                    "pro__body": PRODUCT.get("body"),
                    "pro__summary": PRODUCT.get("summary"),
                    "pro__image": PRODUCT.get("image"),
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
                    "pro__title": PRODUCT.get("title"),
                    "pro__body": PRODUCT.get("body"),
                    "pro__summary": PRODUCT.get("summary"),
                    "pro__image": PRODUCT.get("image"),
                    "pro__tags": PRODUCT.get("tags")
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
