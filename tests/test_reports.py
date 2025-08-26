import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
from datetime import datetime
from db import init_db, DB_PATH
from auth import register_user, login_user
from transactions import add_transaction
from reports import monthly_report, yearly_report

class TestReports(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        register_user("reportuser", "password")
        success, user_id, _ = login_user("reportuser", "password")
        self.user_id = user_id
        # sample data for current month/year
        add_transaction(self.user_id, "income", "Salary", 5000, "Monthly salary")
        add_transaction(self.user_id, "expense", "Food", 1000, "Groceries")
        add_transaction(self.user_id, "expense", "Travel", 500, "Bus pass")

    def test_monthly_report(self):
        now = datetime.now()
        report = monthly_report(self.user_id, now.year, now.month)
        self.assertEqual(report["total_income"], 5000)
        self.assertEqual(report["total_expenses"], 1500)
        self.assertEqual(report["savings"], 3500)

    def test_yearly_report(self):
        now = datetime.now()
        report = yearly_report(self.user_id, now.year)
        self.assertEqual(report["total_income"], 5000)
        self.assertEqual(report["total_expenses"], 1500)
        self.assertEqual(report["savings"], 3500)

if __name__ == "__main__":
    unittest.main()
