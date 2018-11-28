""" This module hosts the test data """
import json

ADMIN_USER = {
    "username": "bettblake08",
    "password": "testpass.A08",
    "invalid_password": "testpass12"
}

PRODUCT = {
    "title": "This is a new product",
    "body": "<p>This is a test body</p>",
    "summy": "This is a summary",
    "image": 1,
    "tags": json.dumps([1])
}
