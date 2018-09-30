""" Test class for Order"""
import unittest
import random
from pprint import pprint
from api import app
from api.database import DatabaseConnection

class OrderViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.db = DatabaseConnection()
        self.db.create_orders_table()
        self.default_orders_url = "/api/v1/orders"
        self.indexed_orders_url = "/api/v1/orders/"
        self.default_order = {"user_id": 1, "item": "Fish", "quantity":1}

    def test_index_page(self):
        """ define test methods for index page. """
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))

    def test_create_order(self):
        """ test post method """
        # random_value = random.randint(1, 1000)
        # order = {"user_id": random_value, "item": "Fish", "quantity":random_value}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 1, "item": "Chips", "quantity":1})
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.headers['Content-Type'], 'application/json')    
        self.assertEqual("Chips", request.json['order']['item'])
        self.assertEqual(1, int(request.json['order']['user_id']))

    def test_create_order_without_item_in_request(self):
        """ test post method by not including item in request """
        del self.default_order['item']
        request = self.app.post(self.default_orders_url, \
        json=self.default_order)
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_quantity(self):
        """ test post method by including an invalid quantity value."""
        self.default_order['quantity'] = "abafhh"
        request = self.app.post(self.default_orders_url, json=self.default_order)
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_userid(self):
        """ test post method by including an invalid user id."""
        self.default_order['user_id'] = "sdd"
        request = self.app.post(self.default_orders_url, json=self.default_order)
        self.assertEqual(request.status_code, 400)

    def test_retrieve_order(self):
        """ test get single order """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": 2, "item": "Liver", "quantity":2}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 2, "item": "Liver", "quantity":2})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request =  self.app.get(new_order_link)
        pprint(request.json)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(created_order_id, request.json['order']['id'])

    def test_retrieve_unavailableorder(self):
        """ test fetch order method by passing an index that's not available """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": 3, "item": "Fish", "quantity":3}
        # request = self.app.post(self.default_orders_url, \
        # json={"user_id": 3, "item": "Chaps", "quantity":3})
        # unavailable_order_id = int(request.json['order']['id']) + 2
        new_order_link = self.indexed_orders_url + "3"
        request = self.app.get(new_order_link)
        self.assertEqual(request.status_code, 404)
        self.assertEqual("Order not found", request.json['order'])

    def test_get_all_orders(self):
        """ test get all orders method """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": "4", "item": "Chaps", "quantity":4}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": "4", "item": "Chaps", "quantity":4}) 
        request = self.app.get(self.default_orders_url)
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['orders']), 0)

    def test_update_order(self):
        """ test update order status """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": 5, "item": "Fish Fillet", "quantity":10}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 5, "item": "Fish Fillet", "quantity":10})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"status":"accepted"})
        self.assertEqual(request.status_code, 200)
        # print(request.json)
        self.assertEqual("accepted", request.json['order']['status'])

    def test_update_user_order(self):
        """ test update user order method """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": random_value, "item": "Fish", "quantity":random_value}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 6, "item": "Mandazi", "quantity":6})
        created_order_id = int(request.json['order']['id'])
        new_order_link = "api/v1/users/orders/" + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"user_id": 6, "item": "Rice + Chapatti", "quantity":"4", "status":"pending"})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("Rice + Chapatti", request.json['order']['item'])
        self.assertEqual(4, request.json['order']['quantity'])

    def test_retrieve_user_order(self):
        """ test get user orders method """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": 4, "item": "Fish", "quantity":random_value}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 7, "item": "Chicken Stir-Fried rice", "quantity":7})
        new_order_link = "api/v1/users/myorders/7"
        request = self.app.get(new_order_link)
        self.assertEqual(request.status_code, 200)
        pprint(request.json)
        self.assertEqual(7, request.json['myorders'][0]['user_id'])
        
    def test_update_order_with_invalid_status_value(self):
        """ test update method by including a wrong status value """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": random_value, "item": "Fish", "quantity":random_value}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 8, "item": "Hot chocolate", "quantity":2})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"status":"unknown"})
        self.assertEqual(request.status_code, 400)

    def test_delete_order(self):
        """ test delete single order """
        # random_value = random.randint(1, 1000)
        # order= {"user_id": random_value, "item": "Fish", "quantity":random_value}
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 9, "item": "Chicken Wings", "quantity":6})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request = self.app.delete(new_order_link)
        self.assertEqual(request.status_code, 200)
        self.assertEqual("order was deleted", request.json['result'])

    def test_delete_unavailable_order(self):
        """ test delete method for an unavailable resource """
        # random_value = random.randint(1, 1000)
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 10, "item": "Chips + Chicken", "quantity":2})
        unavailable_order_id = int(request.json['order']['id']) + 2
        unavailable_order_link = self.indexed_orders_url + str(unavailable_order_id)
        request = self.app.delete(unavailable_order_link)
        pprint(request.json)
        self.assertEqual(request.status_code, 200)
        self.assertEqual("unable to delete order", request.json['result'])

    def tearDown(self):
        """ undo effects of tests. """
        self.db.cursor.execute("DROP TABLE orders")

if __name__ == "__main__":
    unittest.main()
