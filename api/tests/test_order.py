""" Test class for Order"""
import unittest
from api import app
from pprint import pprint

class OrderViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True

        # set up default data to work with
        self.order1 = {"user_id": 1, "item": "chips", "quantity":1}
        self.order2= {"user_id": 2, "item": "Fish", "quantity":2}
        request = self.app.post("/api/v1/orders", json=self.order2)

        # update this id and use it as a reference for other tests
        self.created_order_id = 0 
        self.orders_url = "/api/v1/orders"
        self.single_order_url = self.orders_url
        self.generated_id = 0
        self.counter = 0

    def test_index_page(self):
        """ define test methods for index page. """
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))

    def test_create_order(self):
        """ test post method """
        # check if table is empty before creating
        # is_table_empty = self.app.get('/api/v1/orders')
        # if not is_table_empty.json['orders']:
        # self.counter += 1
        request = self.app.post("/api/v1/orders", json=self.order1)
        # pprint(request.json)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.headers['Content-Type'], 'application/json')    
        self.assertEqual("chips", request.json['order']['item'])
        self.assertEqual(1, int(request.json['order']['user_id']))
        # update the created order id variable
        self.created_order_id = int(request.json['order']['id'])
        self.single_order_url += str(self.created_order_id)
        self.generated_id = int(self.created_order_id) + 5
        # print("created id is "+str(self.created_order_id))
        # print("generated id is "+str(self.generated_id))

    def test_create_order_without_item_in_request(self):
        """ test post method by not including item in request """
        # self.counter += 1
        del self.order1['item']
        request = self.app.post(self.orders_url, json=self.order1)
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_quantity(self):
        # self.counter += 1
        """ test post method by including an invalid quantity value."""
        self.order1['quantity'] = "abafhh"
        request = self.app.post(self.orders_url, json=self.order1)
        self.assertEqual(request.status_code, 400)

    def test_create_order_with_invalid_userid(self):
        # self.counter += 1
        """ test post method by including an invalid user id."""
        self.order1['user_id'] = "sdd"
        request = self.app.post(self.orders_url, json=self.order1)
        self.assertEqual(request.status_code, 400)

    def test_retrieve_order(self):
        """ test get single order """
        # self.counter += 1
        # pprint("running get order in position "+ str(self.counter))
        # request =  self.app.get('/api/v1/orders/%s', self.created_order_id)
        request =  self.app.get('/api/v1/orders/2')
        self.assertEqual(request.status_code, 200)
        # pprint(request.json)
       
        # pprint("id is" + str(request.json['order']['id']))
        # print("created id is "+str(self.created_order_id))
        self.assertEqual(2, request.json['order']['id'])
        # self.assertNotEqual("", request.json['order'])

    def test_retrieve_unavailableorder(self):
        """ test fetch order method by passing an index that's not available """
        # available_orders = self.app.get('/api/v1/orders')
        # generated_id = len(available_orders.json['orders']) + 5
        # request = self.app.get('/api/v1/orders/%s', str(self.generated_id))
        # self.counter += 1
        # pprint("running get unavailable order in position "+ str(self.counter))
        request = self.app.get('/api/v1/orders/2')
        self.assertEqual(2, request.json['order']['id'])

    def test_get_all_orders(self):
        """ test get all orders method """
        request = self.app.get(self.orders_url)
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['orders']), 0)

    def test_update_order(self):
        """ test update order status """
        request = self.app.put('/api/v1/orders/2', \
        json={"status":"accepted"})
        self.assertEqual(request.status_code, 200)
        print(request.json)
        self.assertEqual("accepted", request.json['order']['status'])

    def test_update_user_order(self):
        """ test update user order method """
        # user_order_url = "api/v1/users/orders/" + str(self.created_order_id)
        user_order_url = "api/v1/users/orders/1"
        request = self.app.put(user_order_url, \
        json={"user_id": "1", "item": "Rice + Chapatti", "quantity":"4", "status":"pending"})
        # pprint("url was "+ user_order_url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(1, request.json['order']['id'])
        self.assertEqual("Rice + Chapatti", request.json['order']['item'])

    def test_retrieve_user_order(self):
        """ test get user orders method """
        # request = self.app.get('/api/v1/users/myorders/%s', str(self.created_order_id))
        request = self.app.get('/api/v1/users/myorders/1')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(2, request.json['myorders'][0]['id'])

    def test_update_order_with_invalid_status_value(self):
        """ test update method by including a wrong status value """
        request = self.app.put('/api/v1/orders/1', \
        json={"status":"unknown"})
        self.assertEqual(request.status_code, 400)

    def test_delete_order(self):
        """ test delete single order """
        request = self.app.delete('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)
        # pprint(request.json)
        self.assertEqual("order was deleted", request.json['result'])

    def test_delete_unavailable_order(self):
        """ test delete method for an unavailable resource """
        request = self.app.delete('/api/v1/orders/7')
        # self.assertEqual(request.status_code, 404)
        pprint(request.json)
        self.assertEqual(request.status_code, 200)
        self.assertEqual("unable to delete order", request.json['result'])

    def tearDown(self):
        """ undo effects of tests. """
        # send delete commands.
        # self.db.cursor.execute("DROP TABLE orders")
        # request = self.app.delete('/api/v1/orders/3')
        # request = self.app.delete('/api/v1/orders/2')

if __name__ == "__main__":
    unittest.main()
