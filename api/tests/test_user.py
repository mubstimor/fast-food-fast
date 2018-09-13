""" TESTS FOR USER ROUTES"""
import unittest
from api import app

class UserViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self.app.testing = True
        self.user = {"email": "mubstimor@gmail.com", "password": "1234", "gender":"male"}

    def test_create_user(self):
        """ test create user method """
        request = self.app.post('/api/v1/users', json=self.user)
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
