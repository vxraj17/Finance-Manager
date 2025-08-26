import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
from db import init_db, DB_PATH
from auth import register_user, login_user

class TestAuth(unittest.TestCase):

    def setUp(self):
        # Fresh DB before every test
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()

    def test_registration_success(self):
        success, message = register_user("testuser", "password123")
        self.assertTrue(success)
        self.assertIn("successful", message.lower())

    def test_registration_duplicate(self):
        register_user("duplicate", "pass123")
        success, message = register_user("duplicate", "pass123")
        self.assertFalse(success)
        self.assertIn("exists", message.lower())

    def test_login_success(self):
        register_user("loginuser", "mypassword")
        success, user_id, message = login_user("loginuser", "mypassword")
        self.assertTrue(success)
        self.assertIsNotNone(user_id)
        self.assertIn("successful", message.lower())

    def test_login_invalid_password(self):
        register_user("wrongpass", "correct")
        success, user_id, message = login_user("wrongpass", "incorrect")
        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.assertIn("incorrect", message.lower())

    def test_login_nonexistent_user(self):
        success, user_id, message = login_user("ghost", "anything")
        self.assertFalse(success)
        self.assertIsNone(user_id)
        self.assertIn("not", message.lower())

    # Edge validations you added in auth.register_user
    def test_register_empty_username(self):
        success, message = register_user("", "password123")
        self.assertFalse(success)
        self.assertIn("username", message.lower())

    def test_register_empty_password(self):
        success, message = register_user("newuser", "")
        self.assertFalse(success)
        self.assertIn("password", message.lower())

if __name__ == "__main__":
    unittest.main()
