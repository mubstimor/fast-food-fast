""" Test class for FoodItem"""
import unittest
from api import app
from api.database import DatabaseConnection

class FoodItemViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.db = DatabaseConnection()
        self.db.create_fooditem_table()
        self.app.testing = True
        self.fooditem = {"name": "Millet", "category": "Foods", "price":7000}

    def test_create_fooditem(self):
        """ test create food item """
        request = self.app.post('/api/v1/fooditems', json=self.fooditem)
        self.assertEqual(request.status_code, 201)
        self.assertEqual(request.headers['Content-Type'], 'application/json')
        self.assertEqual(7000, request.json['fooditem']['price'])
        self.assertEqual("Foods", request.json['fooditem']['category'])

    def test_create_duplicate_fooditem(self):
        """ test duplicate food item """
        request = self.app.post('/api/v1/fooditems', json=self.fooditem)
        request = self.app.post('/api/v1/fooditems', json=self.fooditem)
        self.assertEqual(request.status_code, 403)
        self.assertEqual(request.headers['Content-Type'], 'application/json')
        self.assertEqual("Menu Item already exists", request.json['error'])

    def test_create_fooditem_with_invalid_price(self):
        """ test post method by including an invalid price value."""
        self.fooditem['price'] = "xada"
        request = self.app.post('/api/v1/fooditems', json=self.fooditem)
        self.assertEqual(request.status_code, 400)

    def test_retrieve_fooditem(self):
        """ test fetch method """
        request = self.app.post('/api/v1/fooditems', \
        json={"name": "Chips", "category": "Foods", "price":6000})
        created_item_id = int(request.json['fooditem']['id'])
        request = self.app.get('/api/v1/fooditems/' + str(created_item_id))
        self.assertEqual(request.status_code, 200)
        self.assertEqual("Chips", request.json['fooditem']['name'])

    def test_retrieve_unavailablefooditem(self):
        """ test fetch method by passing an index that's not available """
        request = self.app.get('/api/v1/fooditems/11')
        self.assertEqual("not found", request.json['fooditem'])

    def test_get_all_fooditems(self):
        """ test get all fooditems method """
        request = self.app.post('/api/v1/fooditems', \
        json={"name": "Chicken Wings", "category": "Foods", "price":18000})
        request = self.app.get('/api/v1/fooditems')
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['fooditems']), 0)

    def test_update_fooditem(self):
        """ test update food item """
        request = self.app.post('/api/v1/fooditems', \
        json={"name": "Liver", "category": "Foods", "price":8000})
        created_item_id = int(request.json['fooditem']['id'])
        item_url = "/api/v1/fooditems/" + str(created_item_id)
        request = self.app.put(item_url, \
        json={"name": "Fish Fillet", "category": "Foods", "price":9000})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(9000, request.json['fooditem']['price'])

    def test_update_unavailablefooditem(self):
        """ test update unavailable item """
        request = self.app.post('/api/v1/fooditems', \
        json={"name": "Chicken Nuggets", "category": "Foods", "price":12000})
        created_item_id = int(request.json['fooditem']['id']) + 3
        item_url = "/api/v1/fooditems/" + str(created_item_id)
        request = self.app.put(item_url, \
        json={"name": "Fish Fillet", "category": "Foods", "price":9000})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("unable to update item", request.json['fooditem'])

    def test_delete_fooditem(self):
        """ test delete method """
        request = self.app.post('/api/v1/fooditems', \
        json={"name": "Hot Chocolate", "category": "Beverages", "price":8000})
        created_item_id = int(request.json['fooditem']['id'])
        item_url = "/api/v1/fooditems/" + str(created_item_id)
        request = self.app.delete(item_url)
        self.assertEqual(request.status_code, 200)
        self.assertNotEqual("", request.json['result'])

    def test_delete_unavailable_fooditem(self):
        """ test delete method for an unavailable resource """
        request = self.app.delete('/api/v1/fooditems/14')
        self.assertEqual("unable to delete item", request.json['result'])

    def tearDown(self):
        """ undo effects of tests. """
        self.db.cursor.execute("DROP TABLE fooditems")
        self.db.close_connection()

if __name__ == "__main__":
    unittest.main()
