# **📘 Finance Manager – User Manual**

<br>

## 1️⃣ Introduction :
Finance Manager is a Python-based personal finance application that helps users manage income, expenses, budgets, and reports. It supports user authentication with bcrypt for secure login, budget alerts, and database backup & restore. This manual guides you step by step in using the application.

<br>

## 2️⃣ Installation :
Ensure Python 3.10+ is installed.<br>
👉Install dependencies: pip install -r requirements.txt <br>
👉Run the application: python main.py <br>

<br>

## 3️⃣ User Registration & Login
👉On startup, choose Register to create a new account.<br>
👉Provide a username and password (stored securely with hashing).<br>
👉Next time, choose Login with the same credentials.<br>

📷 Example:<br>
✅ Registration successful!<br>

<br>

## 4️⃣ Transactions
👉Add income or expenses.
<br>👉Provide category (Food, Travel, etc.), amount, and description.
<br>👉Edit or delete transactions if required.
<br>👉View all transactions in a structured list.

📷 Example:<br>
Food → ₹200<br>
Travel → ₹500<br>

<br>

# 5️⃣ Budget Management
Set a monthly budget for each category.<br>
👉Alerts : ⚠ Close to limit (≥90% spent)  or  ⚠ Exceeded (spent beyond budget)<br>

📷 Example:<br>
Food → Budget: ₹1000 | Spent: ₹950 | Used: 95% | ⚠ Close to limit<br>

<br>

## 6️⃣ Reports
👉Generate monthly or yearly reports.<br>
👉View total income, expenses, and category-wise breakdown.<br>
👉Helps track financial performance.<br>

📷 Example:<br>
=== Monthly Report (2025-08) ===<br>
Income: ₹5000<br>
Expenses: ₹4200<br>
Savings: ₹800<br>

<br>

## 7️⃣ Backup & Restore
👉Use the Backup option to save your database safely.<br>
👉Use the Restore option to load data from a backup if needed.<br>

📷 Example:<br>
✅ Backup created: backup_2025-08-25.db<br>

<br>

## 8️⃣ Testing<br>
👉Run the built-in test suite: python -m unittest discover tests <br>
👉All modules (auth, budgets, transactions, reports, backups) are covered.<br>

📷 Example:<br>
Ran 14 tests in 5.1s<br>
OK<br>

<br>

## 9️⃣ Exit<br>
👉Use the Exit option to close the program safely.<br>

📷 Example:<br>
Thank you for using Finance Manager. Goodbye!<br>






