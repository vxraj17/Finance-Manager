import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
from db import init_db, DB_PATH
from auth import register_user, login_user
from transactions import add_transaction, view_transactions, update_transaction, delete_transaction

class TestTransactions(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        register_user("txnuser", "password")
        success, user_id, _ = login_user("txnuser", "password")
        self.user_id = user_id

    def test_add_transaction(self):
        msg = add_transaction(self.user_id, "income", "Salary", 1000, "Test Salary")
        self.assertIn("success", msg.lower())
        txns = view_transactions(self.user_id)
        self.assertEqual(len(txns), 1)

    def test_update_transaction(self):
        add_transaction(self.user_id, "expense", "Food", 200, "Lunch")
        txns = view_transactions(self.user_id)
        txn_id = txns[-1][0]  # last transaction id
        msg = update_transaction(txn_id, self.user_id, "expense", "Food", 300, "Dinner")
        self.assertIn("update", msg.lower())
        txns = view_transactions(self.user_id)
        updated = [t for t in txns if t[0] == txn_id][0]
        # Your schema has amount at index 3 in previous steps
        self.assertEqual(updated[3], 300)

    def test_delete_transaction(self):
        add_transaction(self.user_id, "expense", "Travel", 150, "Bus fare")
        txns = view_transactions(self.user_id)
        txn_id = txns[-1][0]
        msg = delete_transaction(txn_id, self.user_id)
        self.assertIn("delete", msg.lower())
        ids_after = [t[0] for t in view_transactions(self.user_id)]
        self.assertNotIn(txn_id, ids_after)

if __name__ == "__main__":
    unittest.main()
