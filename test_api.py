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

    def test010_create_order(self):
        """ test post method """
        request = self.app.post('/api/v1/orders', \
        json={"user_id": "3", "item": "chips", "quantity":"1"})
        self.assertEqual(request.status_code, 201)

    def test020_retrieve_order(self):
        """ test fetch method """
        request = self.app.get('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)

    def test030_update_order(self):
        """ test update method """
        request = self.app.put('/api/v1/orders/1', \
        json={"user_id": "3", "item": "chips", "quantity":"2"})
        self.assertIn('quantity', str(request.data))

    def test040_delete_order(self):
        """ test delete method """
        request = self.app.delete('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)

if __name__ == "__main__":
    unittest.main()
