""" Test class for FoodItem"""
import unittest
from api import app

class FoodItemViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.fooditem = {"name": "Millet", "category": "Foods", "price":7000}

    def test_create_fooditem(self):
        """ test post method """
        # check if table is empty before creating
        is_table_empty = self.app.get('/api/v1/fooditems')
        if not is_table_empty.json['fooditems']:
            request = self.app.post('/api/v1/fooditems', json=self.fooditem)
            self.assertEqual(request.status_code, 201)
            self.assertEqual(request.headers['Content-Type'], 'application/json')
            self.assertEqual(7000, request.json['fooditem']['price'])
            self.assertEqual("Foods", request.json['fooditem']['category'])

    def test_create_fooditem_with_invalid_price(self):
        """ test post method by including an invalid price value."""
        self.fooditem['price'] = "xada"
        request = self.app.post('/api/v1/fooditems', json=self.fooditem)
        self.assertEqual(request.status_code, 400)

    def test_retrieve_fooditem(self):
        """ test fetch method """
        request = self.app.get('/api/v1/fooditems/45')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(45, request.json['fooditem']['id'])

    def test_retrieve_unavailablefooditem(self):
        """ test fetch method by passing an index that's not available """
        request = self.app.get('/api/v1/fooditems/10003')
        self.assertEqual("not found", request.json['fooditem'])

    def test_get_all_fooditems(self):
        """ test get all fooditems method """
        request = self.app.get('/api/v1/fooditems')
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['fooditems']), 0)

    def test_update_fooditem(self):
        """ test update method """
        request = self.app.put('/api/v1/fooditems/46', \
        json={"name": "Fish Fillet", "category": "Foods", "price":9000})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(9000, request.json['fooditem']['price'])

    def test_delete_fooditem(self):
        """ test delete method """
        request = self.app.delete('/api/v1/fooditems/35')
        self.assertEqual(request.status_code, 200)
        self.assertNotEqual("", request.json['result'])

    def test_delete_unavailable_fooditem(self):
        """ test delete method for an unavailable resource """
        request = self.app.delete('/api/v1/fooditems/10')
        self.assertEqual("unable to delete item", request.json['result'])

if __name__ == "__main__":
    unittest.main()
