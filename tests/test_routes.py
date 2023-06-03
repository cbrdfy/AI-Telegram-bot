import unittest
import sys
from os import path

# Add the project root directory to the Python path
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "..")))

from bot_app import app


class RoutesTestCase(unittest.TestCase):
    """
    Tests for routes.py
    """
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_root_endpoint(self):
        # Send a GET request to the root endpoint
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Only POST requests are supported")


if __name__ == '__main__':
    unittest.main()
