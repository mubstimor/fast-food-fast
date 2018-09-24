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
        # print(request.data)
        # self.assertEqual(request.data[1], "chips")

    def test_create_order_without_item_in_request(self):
        """ test post method by not including item in request """
        del self.order['item']
        request = self.app.post('/api/v1/orders', json=self.order)
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_quantity(self):
        """ test post method by including an invalid quantity value."""
        self.order['quantity'] = "abafhh"
        request = self.app.post('/api/v1/orders', json=self.order)
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_userid(self):
        """ test post method by including an invalid user id."""
        self.order['user_id'] = "sdd"
        request = self.app.post('/api/v1/orders', json=self.order)
        self.assertEqual(request.status_code, 400)

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
        self.assertEqual(request.status_code, 200)

    def test_delete_order(self):
        """ test delete method """
        request = self.app.delete('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)

if __name__ == "__main__":
    unittest.main()
