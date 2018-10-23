""" TESTS FOR USER ROUTES"""
import unittest
from api import app
from api.db.database import DatabaseConnection

class UserViewTest(unittest.TestCase):
    """ class defines test methods."""

    def setUp(self):
        """ set default values for class. """
        self.app = app.test_client()
        self._db = DatabaseConnection()
        self._db.create_all_tables()
        self.app.testing = True
        self.user = {"name": "John Doe", "email": "john@example.com",
                     "password": "1234", "gender":"male", "user_type":""}

    def test_create_user(self):
        """ test create user method """
        request = self.app.post('/api/v1/auth/signup', json=self.user)
        self.assertEqual(request.status_code, 201)
        self.assertEqual("john@example.com", request.json['user']['email'])

    def test_create_duplicate_user(self):
        """ test create duplicate user """
        request = self.app.post('/api/v1/auth/signup', json=self.user)
        request = self.app.post('/api/v1/auth/signup', json=self.user)
        self.assertEqual(request.status_code, 409)
        self.assertEqual("user already exists", request.json['message'])

    def test_create_user_with_invalid_email(self):
        """ test post method by not including email in request """
        self.user['email'] = "john"
        request = self.app.post('/api/v1/auth/signup', json=self.user)
        self.assertEqual(request.status_code, 400)

    def test_create_user_invalid_gender(self):
        """ test create user by including a wrong value for gender """
        self.user['gender'] = "mammal"
        request = self.app.post('/api/v1/auth/signup', json=self.user)
        self.assertEqual(request.status_code, 400)

    def test_user_login(self):
        """ test user login method """
        request = self.app.post('/api/v1/auth/signup',
                                json={"name": "Jack Jones",
                                      "email": "jack@example.com",
                                      "password": "1234", "gender":"male",
                                      "user_type":""})
        request = self.app.post('/api/v1/auth/login', \
        json={"email": "jack@example.com", "password": "1234"})
        self.assertEqual(True, request.json['ok'])

    def test_invalid_user_password(self):
        """ test invalid user login password"""
        request = self.app.post('/api/v1/auth/signup',
                                json=self.user)
        request = self.app.post('/api/v1/auth/login',
                                json={"email": "john@example.com",
                                      "password": "12345"})
        self.assertEqual(False, request.json['ok'])

    def test_invalid_user_login_email(self):
        """ test invalid user login email"""
        request = self.app.post('/api/v1/auth/signup',
                                json=self.user)
        request = self.app.post('/api/v1/auth/login', \
        json={"email": "john@example.com", "password": "12345"})
        self.assertEqual(False, request.json['ok'])

    def test_user_login_no_password(self):
        """ test login method by not including password in request """
        request = self.app.post('/api/v1/auth/login',
                                json={"email": "mubstimor@gmail.com"})
        self.assertEqual(request.status_code, 400)

    def tearDown(self):
        """ undo effects of tests. """
        self._db.drop_all_tables()

if __name__ == "__main__":
    unittest.main()
