from db import init_db, backup_db, restore_db
from auth import register_user, login_user
from transactions import add_transaction, view_transactions, update_transaction, delete_transaction
from reports import monthly_report, yearly_report
from budgets import set_budget, view_budgets, budget_performance


def main_menu():
    logged_in_user_id = None

    while True:
        print("\n=== Personal Finance Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            success, message = register_user(username, password)
            print(message)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            success, user_id, message = login_user(username, password)
            print(message)
            if success:
                logged_in_user_id = user_id
                after_login_menu(logged_in_user_id)

        elif choice == "3":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")


# Function to handle actions after user login
def after_login_menu(user_id):
    while True:
        print("\n=== Main Dashboard ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. View Monthly Report")
        print("6. View Yearly Report")
        print("7. Set/View Budgets")
        print("8. View Budget Performance")
        print("10. Restore Database")
        print("11. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            trans_type = input("Enter type (income/expense): ").lower()
            if trans_type not in ("income", "expense"):
                print("❌ Invalid type.")
                continue
            category = input("Enter category: ")
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("❌ Invalid amount.")
                continue
            description = input("Enter description (optional): ")
            print(add_transaction(user_id, trans_type, category, amount, description))

        elif choice == "2":
            transactions = view_transactions(user_id)
            if not transactions:
                print("📭 No transactions found.")
            else:
                print("\nYour Transactions:")
                for t in transactions:
                    print(f"ID:{t[0]} | {t[1]} | {t[2]} | ₹{t[3]} | {t[4]} | {t[5]}")

        elif choice == "3":
            transactions = view_transactions(user_id)
            if not transactions:
                print("📭 No transactions to update.")
                continue
            trans_id = int(input("Enter transaction ID to update: "))
            trans_type = input("Enter new type (income/expense): ").lower()
            category = input("Enter new category: ")
            amount = float(input("Enter new amount: "))
            description = input("Enter new description: ")
            print(update_transaction(trans_id, user_id, trans_type, category, amount, description))

        elif choice == "4":
            transactions = view_transactions(user_id)
            if not transactions:
                print("📭 No transactions to delete.")
                continue
            trans_id = int(input("Enter transaction ID to delete: "))
            print(delete_transaction(trans_id, user_id))

        elif choice == "5":
            year = input("Enter year (YYYY): ")
            month = input("Enter month (1-12): ")
            report = monthly_report(user_id, year, month)
            print("\n=== Monthly Report ===")
            print(f"Total Income: ₹{report['total_income']}")
            print(f"Total Expenses: ₹{report['total_expenses']}")
            print(f"Savings: ₹{report['savings']}")

        elif choice == "6":
            year = input("Enter year (YYYY): ")
            report = yearly_report(user_id, year)
            print("\n=== Yearly Report ===")
            print(f"Total Income: ₹{report['total_income']}")
            print(f"Total Expenses: ₹{report['total_expenses']}")
            print(f"Savings: ₹{report['savings']}")


        elif choice == "7":
            print("\n=== Budget Menu ===")
            print("1. Set Budget")
            print("2. View Budgets")
            sub_choice = input("Enter choice: ")

            if sub_choice == "1":
                month = input("Enter month (YYYY-MM): ")
                category = input("Enter category: ")
                try:
                    amount = float(input("Enter budget amount: "))
                except ValueError:
                    print("❌ Invalid amount.")
                    continue
                print(set_budget(user_id, category, month, amount))

            elif sub_choice == "2":
                month = input("Enter month (YYYY-MM): ")
                budgets = view_budgets(user_id, month)
                if not budgets:
                    print("📭 No budgets set for this month.")
                else:
                    print(f"\n=== Budgets for {month} ===")
                    for b in budgets:
                        print(f"{b[0]} → ₹{b[1]}")
            else:
                print("❌ Invalid choice.")


        elif choice == "8":
            month = input("Enter month (YYYY-MM): ")
            report = budget_performance(user_id, month)
            if not report:
                print("📭 No budgets set for this month.")
            else:
                print(f"\n=== Budget Performance for {month} ===")
                for r in report:
                    print(f"{r['category']} → Budget: ₹{r['budget']} | Spent: ₹{r['spent']} | "
                          f"Remaining: ₹{r['remaining']:.2f} | Used: {r['percent_used']:.1f}% | {r['status']}")


        elif choice == "9":
            print(backup_db())


        elif choice == "10":
            print(restore_db())

        elif choice == "11":
            print("🔓 Logged out.")
            break

        else:
            print("⚠ Feature not implemented yet.")



if __name__ == "__main__":
    init_db()
    main_menu()
