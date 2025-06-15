import unittest
from fastapi import HTTPException
from backend.auth import create_token, verify_token, SECRET_KEY, ALGORITHM
import jwt
import datetime

class TestAuth(unittest.TestCase):

    def test_create_token_validity(self):
        token = create_token("testuser")
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded["sub"], "testuser")
        self.assertIn("exp", decoded)

    def test_verify_token_success(self):
        token = create_token("testuser")
        result = verify_token(token)  # ✅ call directly
        self.assertEqual(result, "testuser")

    def test_verify_token_expired(self):
        expired_time = datetime.datetime.now(datetime.UTC) - datetime.timedelta(seconds=1)
        expired_token = jwt.encode(
            {"sub": "expireduser", "exp": expired_time},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        with self.assertRaises(HTTPException) as context:
            verify_token(expired_token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token expired")

    def test_verify_token_invalid(self):
        invalid_token = "this.is.not.valid"
        with self.assertRaises(HTTPException) as context:
            verify_token(invalid_token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid token")

if __name__ == "__main__":
    unittest.main()
