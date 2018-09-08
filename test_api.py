import unittest
from api import app

class IndexViewTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_page(self):
        index = self.app.get('/')
        self.assertIn('Home', str(index.data))


if __name__ == "__main__":
    unittest.main()
