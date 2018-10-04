""" Test class for Order"""
import unittest
from api import app
from pprint import pprint
from api.database import DatabaseConnection

class OrderViewTest(unittest.TestCase):
    """ class defines test methods."""

    def _set_up_user(self):
        """ get user token """
        request = self.app.post('/api/v1/auth/signup', \
        json={"name": "Jack Decker", "email": "jack@example.com", "password": "1234", "gender":"male", "user_type":""})
        request = self.app.post('/api/v1/auth/login', \
        json={"email": "jack@example.com", "password": "1234"})
        pprint(request.json)
        user_token = "Bearer " +str(request.json['data']['token'])
        return user_token

    def _set_up_admin_token(self):
        """ test admin token """
        request = self.app.post('/api/v1/auth/signup', \
        json={"name": "James Adkins", "email": "james@example.com", "password": "1234", "gender":"male", "user_type":"Admin"})
        request = self.app.post('/api/v1/auth/login', \
        json={"email": "james@example.com", "password": "1234"})
        admin_token = "Bearer " + str(request.json['data']['token'])
        # override
        # admin_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIzMDI2MzBkMC04MzhhLTRjZjctOWRmMC0yNjVkYmUwYThlM2YiLCJleHAiOjE1Mzg2NTUxMTYsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTM4NTY4NzE2LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTM4NTY4NzE2LCJpZGVudGl0eSI6eyJyb2xlIjoiQWRtaW4iLCJpZCI6MSwiZW1haWwiOiJtdWJzdGltb3JAZ21haWwuY29tIn19.RQYuku1D6B2hnPboixGmy78KCmwQ5oEoEL8Z6W0DljM"
        return admin_token
        

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.db = DatabaseConnection()
        self.db.create_orders_table()
        self.default_orders_url = "/api/v1/orders"
        self.indexed_orders_url = "/api/v1/orders/"
        self.default_order = {"user_id": 1, "item": "Fish", "quantity":1}
        self.client_token = self._set_up_user()
        self.admin_token = self._set_up_admin_token()

    def test_index_page(self):
        """ define test methods for index page. """
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))

    def test_create_order(self):
        """ test post method """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 1, "item": "Chips", "quantity":1}, headers={"Authorization": self.client_token})
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.headers['Content-Type'], 'application/json')    
        self.assertEqual("Chips", request.json['order']['item'])
        self.assertEqual(1, int(request.json['order']['user_id']))

    def test_create_already_existing_order(self):
        """ test create duplicate order """
        request = self.app.post(self.default_orders_url, json=self.default_order, headers={"Authorization": self.client_token})
        request = self.app.post(self.default_orders_url, json=self.default_order, headers={"Authorization": self.client_token})
        self.assertEqual(request.status_code, 403)
        self.assertEqual(request.headers['Content-Type'], 'application/json')    
        self.assertEqual("Order already exists", request.json['error'])

    def test_create_order_without_item_in_request(self):
        """ test post method by not including item in request """
        del self.default_order['item']
        request = self.app.post(self.default_orders_url, \
        json=self.default_order, headers={"Authorization": self.client_token})
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_quantity(self):
        """ test post method by including an invalid quantity value."""
        self.default_order['quantity'] = "abafhh"
        request = self.app.post(self.default_orders_url, json=self.default_order, headers={"Authorization": self.client_token})
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_userid(self):
        """ test post method by including an invalid user id."""
        self.default_order['user_id'] = "sdd"
        request = self.app.post(self.default_orders_url, json=self.default_order, headers={"Authorization": self.client_token})
        self.assertEqual(request.status_code, 400)

    def test_retrieve_order(self):
        """ test get single order """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 2, "item": "Liver", "quantity":2}, headers={"Authorization": self.admin_token})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request =  self.app.get(new_order_link, headers={"Authorization": self.admin_token})
        pprint(request.json)
        pprint(self.admin_token)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(created_order_id, request.json['order']['id'])

    def test_retrieve_unavailableorder(self):
        """ test fetch order method by passing an index that's not available """
        new_order_link = self.indexed_orders_url + "3"
        request = self.app.get(new_order_link, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 404)
        self.assertEqual("Order not found", request.json['order'])

    def test_get_all_orders(self):
        """ test get all orders method """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": "4", "item": "Chaps", "quantity":4}) 
        request = self.app.get(self.default_orders_url, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['orders']), 0)

    def test_get_empty_orders_list(self):
        """ test get all orders method """
        request = self.app.get(self.default_orders_url, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("No orders available", request.json['orders'])

    def test_update_order(self):
        """ test update order status """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 5, "item": "Fish Fillet", "quantity":10}, headers={"Authorization": self.admin_token})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"status":"accepted"}, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("accepted", request.json['order']['status'])

    def test_update_unavailable_order(self):
        """ test update order status of unavailable order"""
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 11, "item": "Chicken Nuggets", "quantity":10}, headers={"Authorization": self.admin_token})
        created_order_id = int(request.json['order']['id']) + 3
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"status":"accepted"}, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("unable to update order", request.json['order'])

    def test_update_user_order(self):
        """ test update user order method """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 6, "item": "Mandazi", "quantity":6}, headers={"Authorization": self.client_token})
        created_order_id = int(request.json['order']['id'])
        new_order_link = "api/v1/users/orders/" + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"user_id": 6, "item": "Rice + Chapatti", "quantity":"4", "status":"pending"}, headers={"Authorization": self.client_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("Rice + Chapatti", request.json['order']['item'])
        self.assertEqual(4, request.json['order']['quantity'])

    def test_update_unavailable_user_order(self):
        """ test update unavailable user order """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 12, "item": "Fish", "quantity":6}, headers={"Authorization": self.client_token})
        created_order_id = int(request.json['order']['id']) + 4
        new_order_link = "api/v1/users/orders/" + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"user_id": 6, "item": "Rice + Chapatti", "quantity":"4", "status":"pending"}, headers={"Authorization": self.client_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("unable to update order", request.json['order'])

    def test_retrieve_user_order(self):
        """ test get user orders method """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 7, "item": "Chicken Stir-Fried rice", "quantity":7}, headers={"Authorization": self.client_token})
        new_order_link = "api/v1/users/myorders/7"
        request = self.app.get(new_order_link, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(7, request.json['myorders'][0]['user_id'])
        
    def test_update_order_with_invalid_status_value(self):
        """ test update method by including a wrong status value """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 8, "item": "Hot chocolate", "quantity":2}, headers={"Authorization": self.admin_token})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request = self.app.put(new_order_link, \
        json={"status":"unknown"}, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 400)

    def test_delete_order(self):
        """ test delete single order """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 9, "item": "Chicken Wings", "quantity":6}, headers={"Authorization": self.admin_token})
        created_order_id = int(request.json['order']['id'])
        new_order_link = self.indexed_orders_url + str(created_order_id)
        request = self.app.delete(new_order_link, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("order was deleted", request.json['result'])

    def test_delete_unavailable_order(self):
        """ test delete method for an unavailable resource """
        request = self.app.post(self.default_orders_url, \
        json={"user_id": 10, "item": "Chips + Chicken", "quantity":2}, headers={"Authorization": self.admin_token})
        unavailable_order_id = int(request.json['order']['id']) + 2
        unavailable_order_link = self.indexed_orders_url + str(unavailable_order_id)
        request = self.app.delete(unavailable_order_link, headers={"Authorization": self.admin_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("unable to delete order", request.json['result'])

    def tearDown(self):
        """ undo effects of tests. """
        self.db.cursor.execute("DROP TABLE orders")
        self.db.close_connection()

if __name__ == "__main__":
    unittest.main()
