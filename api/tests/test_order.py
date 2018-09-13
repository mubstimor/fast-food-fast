""" Test class for project"""
import unittest
from api import app

class OrderViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.order = {"user_id": 1, "item": "chips", "quantity":1}

    def test_index_page(self):
        """ define test methods for index page. """
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))

    def test_create_order(self):
        """ test post method """
        request = self.app.post('/api/v1/orders', json=self.order)
        self.assertEqual(request.status_code, 201)

    def test_retrieve_order(self):
        """ test fetch method """
        self.test_create_order()
        request = self.app.get('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)

    def test_get_all_orders(self):
        """ test get all orders method """
        request = self.app.get('/api/v1/orders')
        self.assertEqual(request.status_code, 200)

    def test_update_order(self):
        """ test update method """
        self.test_create_order()
        request = self.app.put('/api/v1/orders/1', \
        json={"status":"accepted"})
        self.assertIn('status', str(request.data))

    def test_delete_order(self):
        """ test delete method """
        request = self.app.delete('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)

if __name__ == "__main__":
    unittest.main()
