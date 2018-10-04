""" Test class for FoodItem"""
import unittest
import json
from pprint import pprint
from api import app
from api.database import DatabaseConnection

class FoodItemViewTest(unittest.TestCase):
    """ class defines test methods."""

    def _set_up_admin_token(self):
        """ test admin token """
        request = self.app.post('/api/v1/auth/signup', \
        json={"name": "James Adkins", "email": "james@example.com", "password": "1234", "gender":"male", "user_type":"Admin"})
        request = self.app.post('/api/v1/auth/login', \
        json={"email": "james@example.com", "password": "1234"})
        admin_token = "Bearer " + str(request.json['data']['token'])
        return admin_token

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.db = DatabaseConnection()
        self.db.create_fooditem_table()
        self.app.testing = True
        self.fooditem = {"name": "Millet", "category": "Foods", "price":7000}
        # self.db.create_users_table()
        # self.admin = {"name": "Jack Cobbsn", "email": "jackobo1@example.com", "password": "1234", "gender":"male"}
        # self.request = self.app.post('/api/v1/auth/signup', json=self.admin)
        
        # self.created_user_id=0
        # pprint(self.request.json)
        # if self.request.json['error']== "user already exists":
        #     # get id existing user
        #     user_url = '/api/v1/users/admin/' + self.admin['email']
        #     request = self.app.get(user_url)
        #     self.created_user_id = request.json['id']
            
        # else:
        #     self.created_user_id = int(self.request.json['user']['id'])
        # pprint(self.created_user_id)
        # # self.created_user_id = int(self.request.json['user']['id'])
        # # self.db.drop_users_table()
        # self.user_uri = '/api/v1/users/' + str(self.created_user_id)
        # request = self.app.put(self.user_uri)
        # # pprint(request.json)
        # # login
        # self.request = self.app.post('/api/v1/auth/login', \
        # json={"email": "jackob1@example.com", "password": "1234"})
        # # pprint(self.request.json)
        # # self.admin_token = str(self.request.json['access_token'])
        # # token unusable
        # # pprint(self.admin_token)
        
        # self.admin_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4OGQzODdjYy04YTdhLTRmZjAtODI3MC03ZmQzNjNiY2NjZDQiLCJleHAiOjE1Mzg2NDc5MTUsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTM4NTYxNTE1LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTM4NTYxNTE1LCJpZGVudGl0eSI6eyJyb2xlIjoiQWRtaW4iLCJpZCI6MSwiZW1haWwiOiJtdWJzdGltb3JAZ21haWwuY29tIn19.h_jR6izQoEJ_MLy0Cts47_a-IMonbplWaOOxLkTy5zY"
        # # self.admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMjY5YWNmNy0zYzQ2LTRhYjYtODc2MC03ZmRmY2QxYjRmZDIiLCJleHAiOjE1Mzg2MjQyMDEsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTM4NTM3ODAxLCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTM4NTM3ODAxLCJpZGVudGl0eSI6eyJyb2xlIjoiQWRtaW4iLCJpZCI6MSwiZW1haWwiOiJtdWJzdGltb3JAZ21haWwuY29tIn19.HcnepeJG_YKDIlftb0qGYC8hRCzmj0Re385xX-AcqwU"
        # self.bearer_token = "Bearer " + self.admin_token
        self.bearer_token = self._set_up_admin_token()

    def test_create_fooditem(self):
        """ test create food item """
        data = json.dumps(self.fooditem)
        request = self.app.post('/api/v1/menu', json=self.fooditem, headers={"Authorization": self.bearer_token})
        pprint(request.json)
        self.assertEqual(request.status_code, 201)  
        self.assertEqual(request.headers['Content-Type'], 'application/json')
        self.assertEqual(7000, request.json['fooditem']['price'])
        self.assertEqual("Foods", request.json['fooditem']['category'])

    def test_create_duplicate_menuitem(self):
        """ test duplicate menu item """
        request = self.app.post('/api/v1/menu', json=self.fooditem, headers={"Authorization": self.bearer_token})
        request = self.app.post('/api/v1/menu', json=self.fooditem, headers={"Authorization": self.bearer_token})
        self.assertEqual(request.status_code, 403)
        self.assertEqual(request.headers['Content-Type'], 'application/json')
        self.assertEqual("Menu Item already exists", request.json['error'])

    def test_create_menuitem_with_invalid_price(self):
        """ test post method by including an invalid price value."""
        self.fooditem['price'] = "xada"
        request = self.app.post('/api/v1/menu', json=self.fooditem, headers={"Authorization": self.bearer_token})
        self.assertEqual(request.status_code, 400)

    def test_retrieve_menuitem(self):
        """ test fetch method """
        request = self.app.post('/api/v1/menu', \
        json={"name": "Chips", "category": "Foods", "price":6000}, headers={"Authorization": self.bearer_token})
        pprint(request.json)
        created_item_id = int(request.json['fooditem']['id'])
        request = self.app.get('/api/v1/menu/' + str(created_item_id))
        self.assertEqual(request.status_code, 200)
        self.assertEqual("Chips", request.json['fooditem']['name'])

    def test_retrieve_unavailablemenuitem(self):
        """ test fetch method by passing an index that's not available """
        request = self.app.get('/api/v1/menu/11')
        self.assertEqual("not found", request.json['fooditem'])

    def test_get_all_menuitems(self):
        """ test get all menuitems method """
        request = self.app.post('/api/v1/menu', \
        json={"name": "Chicken Wings", "category": "Foods", "price":18000}, headers={"Authorization": self.bearer_token})
        request = self.app.get('/api/v1/menu')
        self.assertEqual(request.status_code, 200)
        self.assertGreater(len(request.json['fooditems']), 0)

    def test_update_menuitem(self):
        """ test update food item """
        request = self.app.post('/api/v1/menu', \
        json={"name": "Liver", "category": "Foods", "price":8000}, headers={"Authorization": self.bearer_token})
        created_item_id = int(request.json['fooditem']['id'])
        item_url = "/api/v1/menu/" + str(created_item_id)
        request = self.app.put(item_url, \
        json={"name": "Fish Fillet", "category": "Foods", "price":9000}, headers={"Authorization": self.bearer_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(9000, request.json['fooditem']['price'])

    def test_update_unavailablemenuitem(self):
        """ test update unavailable item """
        request = self.app.post('/api/v1/menu', \
        json={"name": "Chicken Nuggets", "category": "Foods", "price":12000}, headers={"Authorization": self.bearer_token})
        created_item_id = int(request.json['fooditem']['id']) + 3
        item_url = "/api/v1/menu/" + str(created_item_id)
        request = self.app.put(item_url, \
        json={"name": "Fish Fillet", "category": "Foods", "price":9000}, headers={"Authorization": self.bearer_token})
        self.assertEqual(request.status_code, 200)
        self.assertEqual("unable to update item", request.json['fooditem'])

    def test_delete_menuitem(self):
        """ test delete method """
        request = self.app.post('/api/v1/menu', \
        json={"name": "Hot Chocolate", "category": "Beverages", "price":8000}, headers={"Authorization": self.bearer_token})
        created_item_id = int(request.json['fooditem']['id'])
        item_url = "/api/v1/menu/" + str(created_item_id)
        request = self.app.delete(item_url, headers={"Authorization": self.bearer_token})
        self.assertEqual(request.status_code, 200)
        self.assertNotEqual("", request.json['result'])

    def test_delete_unavailable_menuitem(self):
        """ test delete method for an unavailable resource """
        request = self.app.delete('/api/v1/menu/14', headers={"Authorization": self.bearer_token})
        self.assertEqual("unable to delete item", request.json['result'])

    def tearDown(self):
        """ undo effects of tests. """
        self.db.cursor.execute("DROP TABLE fooditems")
        # self.db.cursor.execute("DROP TABLE users")
        self.db.close_connection()

if __name__ == "__main__":
    unittest.main()
