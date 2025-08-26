📘 Finance Manager – User Manual

1️⃣ Introduction : Finance Manager is a Python-based personal finance application that helps users manage income, expenses, budgets, and reports. It supports user authentication with bcrypt for secure login, budget alerts, and database backup & restore. This manual guides you step by step in using the application.



2️⃣ Installation : Ensure Python 3.10+ is installed.
-Install dependencies:
    -pip install -r requirements.txt
-Run the application:
    -python main.py



3️⃣ User Registration & Login
-On startup, choose Register to create a new account.
-Provide a username and password (stored securely with hashing).
-Next time, choose Login with the same credentials.

📷 Example:
✅ Registration successful!



4️⃣ Transactions
-Add income or expenses.
-Provide category (Food, Travel, etc.), amount, and description.
-Edit or delete transactions if required.
-View all transactions in a structured list.

📷 Example:
Food → ₹200
Travel → ₹500



5️⃣ Budget Management
-Set a monthly budget for each category.
-Alerts:
    -⚠ Close to limit (≥90% spent)
    -⚠ Exceeded (spent beyond budget)

📷 Example:
Food → Budget: ₹1000 | Spent: ₹950 | Used: 95% | ⚠ Close to limit



6️⃣ Reports
-Generate monthly or yearly reports.
-View total income, expenses, and category-wise breakdown.
-Helps track financial performance.

📷 Example:
=== Monthly Report (2025-08) ===
Income: ₹5000
Expenses: ₹4200
Savings: ₹800



7️⃣ Backup & Restore
-Use Backup option to save your database safely.
-Use Restore option to load data from a backup if needed.

📷 Example:
✅ Backup created: backup_2025-08-25.db



8️⃣ Testing
Run the built-in test suite:
 -python -m unittest discover tests
All modules (auth, budgets, transactions, reports, backups) are covered.

📷 Example:
Ran 14 tests in 5.1s
OK



9️⃣ Exit
-Use the Exit option to close the program safely.

📷 Example:
Thank you for using Finance Manager. Goodbye!
