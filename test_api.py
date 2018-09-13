""" Test class for project"""
import unittest
from api import app

class IndexViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.user = {"email": "mubstimor@gmail.com", "password": "1234", "gender":"male"}
        # self.test_create_user()

    def test_index_page(self):
        """ define test methods for index page. """
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))

    def test_create_order(self):
        """ test post method """
        request = self.app.post('/api/v1/orders', \
        json={"user_id": "3", "item": "chips", "quantity":"1"})
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
        json={"user_id": "3", "item": "chips", "status":"accepted", "quantity":"2"})
        self.assertIn('quantity', str(request.data))

    def test_delete_order(self):
        """ test delete method """
        request = self.app.delete('/api/v1/orders/1')
        self.assertEqual(request.status_code, 200)

    # TESTS FOR USER ROUTES

    def test_create_user(self):
        """ test create user method """
        request = self.app.post('/api/v1/users', \
        json=self.user)
        self.assertEqual(request.status_code, 201)

    def test_user_login(self):
        """ test user login method """
        request = self.app.post('/api/v1/users/login', \
        json={"email": "mubstimor@gmail.com", "password": "1234"})
        self.assertIn('success', str(request.data))

    def test_get_user(self):
        """ test get user method """
        request = self.app.get('/api/v1/users/1')
        self.assertEqual(request.status_code, 200)

    def test_get_all_users(self):
        """ test get user method """
        request = self.app.get('/api/v1/users')
        self.assertEqual(request.status_code, 200)

if __name__ == "__main__":
    unittest.main()
