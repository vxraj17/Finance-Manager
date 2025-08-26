from db import get_connection
from datetime import datetime
from budgets import check_budget


# Function to add a new transaction
def add_transaction(user_id, trans_type, category, amount, description=""):
    """Add a new income or expense transaction, with budget check for expenses."""
    conn = get_connection()
    cursor = conn.cursor()

    date_str = datetime.now().strftime("%Y-%m-%d")
    month_str = datetime.now().strftime("%Y-%m")

    # Budget check (only for expenses)
    budget_message = ""
    if trans_type == "expense":
        budget, spent = check_budget(user_id, category, month_str)
        if budget is not None:
            new_total = spent + amount
            if new_total >= budget:
                budget_message = f"⚠ WARNING: Budget exceeded or completed for {category} in {month_str}! (Limit: ₹{budget}, Spent: ₹{new_total})"
            elif new_total >= 0.9 * budget:  # ✅ fixed to include exactly 90%
                budget_message = f"⚠ ALERT: You are close to exceeding your budget for {category} in {month_str}. (Limit: ₹{budget}, Spent: ₹{new_total})"

    # Insert transaction
    cursor.execute("""
        INSERT INTO transactions (user_id, type, category, amount, date, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, trans_type, category, amount, date_str, description))

    conn.commit()
    conn.close()

    return "✅ Transaction added successfully!" + (f"\n{budget_message}" if budget_message else "")



# Function to view all transactions for a user
def view_transactions(user_id):
    """Return all transactions for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, category, amount, date, description
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# Function to update an existing transaction
def update_transaction(transaction_id, user_id, trans_type, category, amount, description):
    """Update a transaction if it belongs to the user."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET type = ?, category = ?, amount = ?, description = ?
        WHERE id = ? AND user_id = ?
    """, (trans_type, category, amount, description, transaction_id, user_id))

    conn.commit()
    conn.close()
    return "✅ Transaction updated successfully!"


# Function to delete a transaction
def delete_transaction(transaction_id, user_id):
    """Delete a transaction if it belongs to the user."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?",
                   (transaction_id, user_id))

    conn.commit()
    conn.close()
    return "🗑 Transaction deleted successfully!"

