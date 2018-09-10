""" Test class for project"""
import unittest
from api import app

class IndexViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        """ define test methods for index page. """
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))

    def test_create_order(self):
        """ test post method """
        request = self.app.post('/api/v1/orders', \
        json={"user_id": 3, "item": "chips", "quantity":1})
        self.assertEqual(request.status_code, 201)

if __name__ == "__main__":
    unittest.main()
