import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
from datetime import datetime
from db import init_db, DB_PATH
from auth import register_user, login_user
from transactions import add_transaction
from reports import monthly_report

class TestReportEdgeCases(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        register_user("edge_report_user", "password")
        success, user_id, _ = login_user("edge_report_user", "password")
        self.user_id = user_id
        self.now = datetime.now()

    def test_no_transactions(self):
        r = monthly_report(self.user_id, self.now.year, self.now.month)
        self.assertEqual(float(r["total_income"]), 0.0)
        self.assertEqual(float(r["total_expenses"]), 0.0)
        self.assertEqual(float(r["savings"]), 0.0)

    def test_only_income(self):
        add_transaction(self.user_id, "income", "Salary", 3000, "Test salary")
        r = monthly_report(self.user_id, self.now.year, self.now.month)
        self.assertEqual(float(r["total_income"]), 3000.0)
        self.assertEqual(float(r["total_expenses"]), 0.0)
        self.assertEqual(float(r["savings"]), 3000.0)

    def test_only_expenses(self):
        add_transaction(self.user_id, "expense", "Food", 500, "Groceries")
        r = monthly_report(self.user_id, self.now.year, self.now.month)
        self.assertEqual(float(r["total_income"]), 0.0)
        self.assertEqual(float(r["total_expenses"]), 500.0)
        self.assertEqual(float(r["savings"]), -500.0)

if __name__ == "__main__":
    unittest.main()
