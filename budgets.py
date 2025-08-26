from db import get_connection


# Function to set or update a budget for a user
def set_budget(user_id, category, month, amount):
    """Set or update a monthly budget for a category (month stored as YYYY-MM)."""
    # Normalize month input to YYYY-MM
    parts = month.split("-")
    if len(parts) == 2:
        year, m = parts
        month = f"{year}-{int(m):02}"  # force 2-digit month

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO budgets (user_id, category, month, amount)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, category, month)
            DO UPDATE SET amount = excluded.amount
        """, (user_id, category, month, amount))
        conn.commit()
        conn.close()
        return f"✅ Budget set for {category} in {month}: ₹{amount}"
    except Exception as e:
        conn.close()
        return f"❌ Error: {str(e)}"


# Function to view budgets for a specific month
def view_budgets(user_id, month):
    """View all budgets for a given month."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, amount
        FROM budgets
        WHERE user_id = ? AND month = ?
    """, (user_id, month))
    rows = cursor.fetchall()
    conn.close()
    return rows


# Check budget function to compare expenses with budget
def check_budget(user_id, category, month):
    """Check current expenses vs budget for a category in a month."""
    conn = get_connection()
    cursor = conn.cursor()

    # Get budget (if any)
    cursor.execute("""
        SELECT amount FROM budgets
        WHERE user_id = ? AND category = ? AND month = ?
    """, (user_id, category, month))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None, 0  # No budget set for this category

    budget_amount = row[0]

    # Get total expenses so far in this month for this category
    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ? AND category = ? 
              AND type = 'expense'
              AND strftime('%Y-%m', date) = ?
    """, (user_id, category, month))
    spent = cursor.fetchone()[0]

    conn.close()
    return budget_amount, spent


# Function to show budget performance for a user in a specific month
def budget_performance(user_id, month):
    """Show budget vs actual spending for all categories in a given month."""
    # Normalize month
    parts = month.split("-")
    if len(parts) == 2:
        year, m = parts
        month = f"{year}-{int(m):02}"

    conn = get_connection()
    cursor = conn.cursor()

    # Get all budgets for this month
    cursor.execute("""
        SELECT category, amount
        FROM budgets
        WHERE user_id = ? AND month = ?
    """, (user_id, month))
    budgets = cursor.fetchall()

    report = []
    for category, budget_amount in budgets:
        # Total spent in this category
        cursor.execute("""
            SELECT IFNULL(SUM(amount), 0)
            FROM transactions
            WHERE user_id = ? AND category = ?
                  AND type = 'expense'
                  AND strftime('%Y-%m', date) = ?
        """, (user_id, category, month))
        spent = cursor.fetchone()[0]

        remaining = budget_amount - spent
        percent_used = (spent / budget_amount * 100) if budget_amount > 0 else 0

        status = "✅ OK"
        if spent > budget_amount:
            status = "⚠ Exceeded"
        elif spent >= 0.9 * budget_amount:
            status = "⚠ Close to limit"

        report.append({
            "category": category,
            "budget": budget_amount,
            "spent": spent,
            "remaining": remaining,
            "percent_used": percent_used,
            "status": status
        })

    conn.close()
    return report
