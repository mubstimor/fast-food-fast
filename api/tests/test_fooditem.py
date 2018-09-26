""" Test class for FoodItem"""
import unittest
from api import app

class FoodItemViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.fooditem = {"name": "Chips", "category": "Foods", "price":7000}

    def test_create_fooditem(self):
        """ test post method """
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
        self.fooditem['name'] = "Rice"
        self.test_create_fooditem()
        request = self.app.get('/api/v1/fooditems/1')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(1, request.json['fooditem']['id'])

    def test_retrieve_unavailablefooditem(self):
        """ test fetch method by passing an index that's not available """
        self.fooditem['name'] = "Chapatti"
        self.test_create_fooditem()
        request = self.app.get('/api/v1/fooditems/89')
        self.assertEqual(request.status_code, 404)

    def test_get_all_fooditems(self):
        """ test get all fooditems method """
        self.fooditem['name'] = "Fish"
        self.test_create_fooditem()
        request = self.app.get('/api/v1/fooditems')
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['fooditems']), 0)

    def test_update_fooditem(self):
        """ test update method """
        self.fooditem['name'] = "Liver"
        self.test_create_fooditem()
        request = self.app.put('/api/v1/fooditems/1', \
        json={"name": "Fish Fillet", "category": "Foods", "price":9000})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(1, request.json['fooditem']['id'])
        self.assertEqual("Fish Fillet", request.json['fooditem']['name'])
        self.assertEqual(9000, request.json['fooditem']['price'])

    def test_delete_fooditem(self):
        """ test delete method """
        request = self.app.delete('/api/v1/fooditems/1')
        self.assertEqual(request.status_code, 200)
        self.assertEqual("fooditem was deleted", request.json['result'])

    def test_delete_unavailable_fooditem(self):
        """ test delete method for an unavailable resource """
        request = self.app.delete('/api/v1/fooditems/10')
        self.assertEqual(request.status_code, 404)

if __name__ == "__main__":
    unittest.main()
