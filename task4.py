import csv
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
HEADERS = ["id", "date", "description", "amount", "category"]

# Ensure CSV exists
def ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

# Add expense
def add_expense():
    desc = input("Enter description: ")
    amount = input("Enter amount: ")
    category = input("Enter category: ")

    try:
        amt = float(amount)
    except ValueError:
        print("❌ Invalid amount!")
        return

    if not category.strip():
        print("❌ Category cannot be empty!")
        return

    row = [
        str(int(datetime.now().timestamp() * 1000)),
        datetime.now().strftime("%Y-%m-%d"),
        desc,
        f"{amt:.2f}",
        category.strip().title()
    ]

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

    print("✅ Expense added successfully!")

# View all expenses
def view_all():
    ensure_csv()

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if len(rows) <= 1:
        print("⚠️ No expenses found.")
        return

    total = 0
    print("\nID | DATE | DESCRIPTION | AMOUNT | CATEGORY")
    print("-" * 60)

    for r in rows[1:]:
        print(f"{r[0]} | {r[1]} | {r[2]} | ₹{r[3]} | {r[4]}")
        total += float(r[3])

    print(f"\n💰 Total Spent: ₹{total:.2f}")

# Search by category
def search_category():
    cat = input("Enter category: ")

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:]

    results = [r for r in rows if r[4].lower() == cat.lower()]

    if not results:
        print("⚠️ No records found.")
        return

    subtotal = 0
    for r in results:
        print(f"{r[0]} | {r[1]} | {r[2]} | ₹{r[3]} | {r[4]}")
        subtotal += float(r[3])

    print(f"\n📊 Subtotal for {cat}: ₹{subtotal:.2f}")

# Monthly total
def monthly_total():
    month = input("Enter month (YYYY-MM): ")

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:]

    filt = [r for r in rows if r[1].startswith(month)]

    if not filt:
        print("⚠️ No records for this month.")
        return

    total = sum(float(r[3]) for r in filt)
    print(f"📅 Monthly Total for {month}: ₹{total:.2f}")

# Delete by ID
def delete_expense():
    exp_id = input("Enter ID to delete: ")

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    new_rows = [rows[0]] + [r for r in rows[1:] if r[0] != exp_id]

    if len(new_rows) == len(rows):
        print("❌ ID not found!")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(new_rows)

    print("🗑️ Expense deleted successfully!")

# Menu
def run():
    ensure_csv()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All")
        print("3. Search by Category")
        print("4. Monthly Total")
        print("5. Delete by ID")
        print("6. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all()
        elif choice == "3":
            search_category()
        elif choice == "4":
            monthly_total()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    run()