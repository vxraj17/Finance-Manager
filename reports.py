from db import get_connection

def monthly_report(user_id, year, month):
    """Generate total income, expenses, and savings for a specific month."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total income
    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0) 
        FROM transactions
        WHERE user_id = ? AND type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    """, (user_id, str(year), f"{int(month):02}"))
    total_income = cursor.fetchone()[0]

    # Total expenses
    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0) 
        FROM transactions
        WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    """, (user_id, str(year), f"{int(month):02}"))
    total_expenses = cursor.fetchone()[0]

    conn.close()

    # Savings = Income - Expenses
    savings = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings
    }

def yearly_report(user_id, year):
    """Generate total income, expenses, and savings for a specific year."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total income
    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0) 
        FROM transactions
        WHERE user_id = ? AND type = 'income' AND strftime('%Y', date) = ?
    """, (user_id, str(year)))
    total_income = cursor.fetchone()[0]

    # Total expenses
    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0) 
        FROM transactions
        WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ?
    """, (user_id, str(year)))
    total_expenses = cursor.fetchone()[0]

    conn.close()

    savings = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings
    }
