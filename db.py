import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = os.path.join("data", "finance2.db")

# Function to get a database connection
def get_connection():
    """Return a connection to the database."""
    return sqlite3.connect(DB_PATH)

# Function to initialize the database and create necessary tables
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)


    # Budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            UNIQUE(user_id, category, month),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)


    conn.commit()
    conn.close()


# Function to set or update a budget for a user
def backup_db():
    """Create a backup of the database in the backups folder."""
    os.makedirs("backups", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join("backups", f"finance_backup_{timestamp}.db")

    shutil.copy(DB_PATH, backup_file)
    return f"✅ Backup created at {backup_file}"


# Function to restore database from a backup
def restore_db():
    """Restore database from a selected backup file."""
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        return "❌ No backups found."

    backups = [f for f in os.listdir(backup_dir) if f.endswith(".db")]
    if not backups:
        return "❌ No backup files available."

    print("\n=== Available Backups ===")
    for i, backup in enumerate(backups, start=1):
        print(f"{i}. {backup}")

    try:
        choice = int(input("Enter the number of the backup to restore: "))
        if choice < 1 or choice > len(backups):
            return "❌ Invalid choice."
    except ValueError:
        return "❌ Invalid input."

    backup_file = os.path.join(backup_dir, backups[choice - 1])
    shutil.copy(backup_file, DB_PATH)
    return f"✅ Database restored from {backups[choice - 1]}"


if __name__ == "__main__":
    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)
    init_db()
    print("✅ Database initialized successfully.")
