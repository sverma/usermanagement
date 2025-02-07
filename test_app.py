import unittest
import json
from app import app
import app as banking_app  # Import the module to reset globals

class UserManagementTestCase(unittest.TestCase):
    def setUp(self):
        # Enable testing mode and create a test client.
        app.testing = True
        self.client = app.test_client()
        # Reset the in-memory storage and user id counter.
        banking_app.users.clear()
        banking_app.next_user_id = 1

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Banking Platform - User Management API!", response.data)

    def test_create_user(self):
        # Test creating a new user.
        payload = {
            "username": "johndoe",
            "email": "john@example.com",
            "full_name": "John Doe"
        }
        response = self.client.post(
            '/usermanagement/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['username'], "johndoe")
        self.assertEqual(data['email'], "john@example.com")
        self.assertEqual(data['full_name'], "John Doe")
        self.assertEqual(data['id'], "1")

    def test_list_users(self):
        # Create a user first.
        payload = {"username": "johndoe", "email": "john@example.com"}
        self.client.post(
            '/usermanagement/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Retrieve the list of users.
        response = self.client.get('/usermanagement/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_user(self):
        # Create a user.
        payload = {"username": "janedoe", "email": "jane@example.com"}
        response_create = self.client.post(
            '/usermanagement/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data_create = json.loads(response_create.data)
        user_id = data_create['id']
        # Retrieve the specific user.
        response = self.client.get(f'/usermanagement/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], "janedoe")

    def test_update_user(self):
        # Create a user.
        payload = {"username": "janedoe", "email": "jane@example.com"}
        response_create = self.client.post(
            '/usermanagement/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data_create = json.loads(response_create.data)
        user_id = data_create['id']
        # Update the user's email and full_name.
        update_payload = {"email": "newjane@example.com", "full_name": "Jane Doe"}
        response = self.client.put(
            f'/usermanagement/users/{user_id}',
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], "newjane@example.com")
        self.assertEqual(data['full_name'], "Jane Doe")

    def test_delete_user(self):
        # Create a user.
        payload = {"username": "janedoe", "email": "jane@example.com"}
        response_create = self.client.post(
            '/usermanagement/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data_create = json.loads(response_create.data)
        user_id = data_create['id']
        # Delete the user.
        response = self.client.delete(f'/usermanagement/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        # Attempt to retrieve the deleted user.
        response_get = self.client.get(f'/usermanagement/users/{user_id}')
        self.assertEqual(response_get.status_code, 404)

if __name__ == '__main__':
    unittest.main()
