import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os
from db import init_db, DB_PATH
from auth import register_user, login_user
from transactions import add_transaction
from budgets import set_budget, view_budgets, budget_performance

class TestBudgets(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        register_user("budgetuser", "password")
        success, user_id, _ = login_user("budgetuser", "password")
        self.user_id = user_id
        self.month = "2025-08"
        # every test starts with a clean budget
        set_budget(self.user_id, "Food", self.month, 1000)

    def test_set_and_view_budget(self):
        budgets = view_budgets(self.user_id, self.month)
        self.assertTrue(any(b[0] == "Food" and float(b[1]) == 1000 for b in budgets))

    def test_budget_performance_ok(self):
        add_transaction(self.user_id, "expense", "Food", 200, "Snacks")
        report = budget_performance(self.user_id, self.month)
        food = [r for r in report if r["category"] == "Food"][0]
        self.assertEqual(float(food["spent"]), 200)
        self.assertEqual(round(float(food["remaining"]), 2), 800.00)
        self.assertEqual(food["status"], "✅ OK")

    def test_budget_performance_close_to_limit(self):
        add_transaction(self.user_id, "expense", "Food", 950, "Big dinner")
        report = budget_performance(self.user_id, self.month)
        food = [r for r in report if r["category"] == "Food"][0]
        self.assertEqual(food["status"], "⚠ Close to limit")

    def test_budget_performance_exceeded(self):
        add_transaction(self.user_id, "expense", "Food", 1200, "Weekend trip")
        report = budget_performance(self.user_id, self.month)
        food = [r for r in report if r["category"] == "Food"][0]
        self.assertEqual(food["status"], "⚠ Exceeded")

if __name__ == "__main__":
    unittest.main()
