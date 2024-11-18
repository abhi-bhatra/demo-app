import unittest
from src.app import app
import os

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Ensure the database exists before tests
        if not os.path.exists('database.db'):
            from scripts.setup_database import setup_database
            setup_database()

    def test_get_user(self):
        response = self.app.get('/users/testuser')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'password123'
        }
        response = self.app.post('/register',
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_parse_config(self):
        config = """
        server:
          host: localhost
          port: 5000
        """
        response = self.app.post('/parse_config', data=config)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
