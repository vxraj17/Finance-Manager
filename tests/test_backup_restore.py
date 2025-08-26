import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import os, shutil
from db import init_db, DB_PATH, backup_db
from auth import register_user, login_user
from transactions import add_transaction, view_transactions

class TestBackupRestore(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        os.makedirs("backups", exist_ok=True)

    def test_backup_creation(self):
        register_user("backupuser", "password")
        success, user_id, _ = login_user("backupuser", "password")
        add_transaction(user_id, "income", "Salary", 1000, "Initial salary")

        msg = backup_db()
        self.assertIn("backup", msg.lower())
        self.assertIn("created", msg.lower())

        backups = [f for f in os.listdir("backups") if f.endswith(".db")]
        self.assertGreater(len(backups), 0)

    def test_restore_by_copying_latest_backup(self):
        register_user("restoreuser", "password")
        success, user_id, _ = login_user("restoreuser", "password")
        add_transaction(user_id, "income", "Salary", 2000, "First record")

        # make a backup of the 1-transaction state
        backup_db()
        backups = sorted([f for f in os.listdir("backups") if f.endswith(".db")])
        restore_file = os.path.join("backups", backups[-1])

        # add a second transaction (will disappear after restore)
        add_transaction(user_id, "expense", "Food", 500, "Groceries")
        self.assertEqual(len(view_transactions(user_id)), 2)

        # restore by copying the backup over DB_PATH
        shutil.copy(restore_file, DB_PATH)

        # back to 1 transaction
        self.assertEqual(len(view_transactions(user_id)), 1)

if __name__ == "__main__":
    unittest.main()
