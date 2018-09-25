""" Test class for project"""
import unittest
from api import app
# import ast

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
        self.assertEqual(request.headers['Content-Type'], 'application/json')
        self.assertEqual("chips", request.json['order']['item'])
        self.assertEqual(1, request.json['order']['quantity'])

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
        self.order['user_id'] = 7
        self.test_create_order()
        request = self.app.get('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(1, request.json['order']['id'])

    def test_retrieve_unavailableorder(self):
        """ test fetch method by passing an index that's not available """
        self.order['user_id'] = 8
        self.test_create_order()
        request = self.app.get('/api/v1/orders/89')
        self.assertEqual(request.status_code, 404)

    def test_get_all_orders(self):
        """ test get all orders method """
        self.order['user_id'] = 9
        self.test_create_order()
        request = self.app.get('/api/v1/orders')
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['orders']), 0)

    def test_update_order(self):
        """ test update method """
        self.order['user_id'] = 10
        self.test_create_order()
        request = self.app.put('/api/v1/orders/1', \
        json={"status":"accepted"})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(1, request.json['order']['id'])
        self.assertEqual("accepted", request.json['order']['status'])

    def test_update_order_with_invalid_status_value(self):
        """ test update method by including a wrong status value """
        request = self.app.put('/api/v1/orders/1', \
        json={"status":"unknown"})
        self.assertEqual(request.status_code, 400)

    def test_delete_order(self):
        """ test delete method """
        request = self.app.delete('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)
        self.assertEqual("Order was deleted", request.json['result'])

    def test_delete_unavailable_order(self):
        """ test delete method for an unavailable resource """
        request = self.app.delete('/api/v1/orders/1')
        self.assertEqual(request.status_code, 404)

if __name__ == "__main__":
    unittest.main()
