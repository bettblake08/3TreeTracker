from flask import json

from app.tests.v1.test_config import AdminAPITestCase
from app.tests.v1.test_data import PRODUCT


class TestUpdateProductEndpoint(AdminAPITestCase):
    
    def update_product(self, data, product_id):
        return self.test_client.put(
            '/api/v1/admin/product/{}'.format(product_id),
            data=data,
            content_type='application/json'
        )

    def test_using_no_title_field(self):
        response = self.update_product(
            product_id=1,
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
        response = self.update_product(
            product_id=1,
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
        response = self.update_product(
            product_id=1,
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
        response = self.update_product(
            product_id=1,
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
        response = self.update_product(
            product_id=1,
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

        response = self.update_product(
            product_id=1,
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
            "Image does not exist!",
            "Unexpected response message!")

    def test_using_invalid_tag_array(self):

        response = self.update_product(
            product_id=1,
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

    def test_using_invalid_id(self):

        response = self.update_product(
            product_id="ro",
            data=json.dumps(
                {
                    "pro__title": PRODUCT.get("title"),
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

    def test_using_unexisting_product_id(self):

        response = self.update_product(
            product_id=999,
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
            404,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "Product does not exist!",
            "Unexpected response message!")

    def test_using_valid_data(self):

        response = self.update_product(
            product_id=1,
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
            200,
            "Unexpected response status!")

        self.assertEqual(
            data['message'],
            "You have successfully updated the product!",
            "Unexpected response message!")
