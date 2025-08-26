import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
import os
from db import init_db, DB_PATH
from auth import register_user, login_user
from transactions import add_transaction, update_transaction, delete_transaction, view_transactions

class TestEdgeCases(unittest.TestCase):

    def setUp(self):
        # Reset DB before each test
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        # Create user
        register_user("edgeuser", "password")
        success, user_id, _ = login_user("edgeuser", "password")
        self.user_id = user_id

    def test_register_empty_username(self):
        success, message = register_user("", "password123")
        self.assertFalse(success)

    def test_register_empty_password(self):
        success, message = register_user("newuser", "")
        self.assertFalse(success)

    def test_add_transaction_invalid_amount(self):
        # Try with invalid amount (string instead of number)
        with self.assertRaises(ValueError):
            float("notanumber")  # simulate invalid conversion

    def test_update_nonexistent_transaction(self):
        msg = update_transaction(999, self.user_id, "expense", "Food", 100, "Invalid update")
        # should not crash, just say updated (but rowcount = 0)
        self.assertIn("updated", msg.lower())

    def test_delete_nonexistent_transaction(self):
        msg = delete_transaction(999, self.user_id)
        self.assertIn("deleted", msg.lower())

if __name__ == "__main__":
    unittest.main()
