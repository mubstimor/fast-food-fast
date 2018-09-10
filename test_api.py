""" Test class for project"""
import unittest
from api import app
from flask import json

class IndexViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.order = {"user_id": 3, "item": "chips", "quantity":1}

    def test_index_page(self):
        """ define test methods for index page. """
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))

    def test_create_order(self):
        """ test post method """
        # request = {"user_id": "3", "item": "chips", "quantity":"1"}
        post = self.app.post('/api/v1/orders', data=json.dumps(self.order, ensure_ascii=False))
        self.assertEqual(post.status_code, 201)

if __name__ == "__main__":
    unittest.main()
