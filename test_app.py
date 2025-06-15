import unittest
from unittest.mock import patch, mock_open
from fastapi.testclient import TestClient
from fastapi import HTTPException
from backend.app import app, verify_token, call_model, load_users, create_token

client = TestClient(app)

# ✅ Dependency override for FastAPI's Depends
def mock_verify_token():
    return "mockuser"

class TestApp(unittest.TestCase):

    def setUp(self):
        app.dependency_overrides = {
            verify_token: mock_verify_token
        }

    def tearDown(self):
        app.dependency_overrides = {}

    @patch("backend.app.USERS_FILE", "mock_users.json")
    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_signup_success(self, mock_file):
        response = client.post("/signup", data={"username": "alice", "password": "123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    @patch("backend.app.load_users", return_value={"alice": "123"})
    def test_signup_duplicate_user(self, mock_load_users):
        response = client.post("/signup", data={"username": "alice", "password": "123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("User already exists", response.text)

    @patch("backend.app.load_users", return_value={"bob": "pass"})
    @patch("backend.app.create_token", return_value="mocktoken")
    def test_login_success(self, mock_create_token, mock_load_users):
        response = client.post("/login", data={"username": "bob", "password": "pass"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    @patch("backend.app.load_users", return_value={"bob": "pass"})
    def test_login_invalid(self, mock_load_users):
        response = client.post("/login", data={"username": "bob", "password": "wrong"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid credentials", response.text)

    @patch("backend.app.call_model", return_value=("mock response", 0.123))
    def test_chat_endpoint(self, mock_call_model):
        response = client.post("/chat", data={"prompt": "Hello"}, headers={"Authorization": "Bearer mocktoken"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())
        self.assertEqual(response.json()["response"], "mock response")

    def test_metrics(self):
        response = client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn("requests", response.json())
        self.assertIn("model", response.json())

if __name__ == "__main__":
    unittest.main()
