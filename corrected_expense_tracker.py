import csv

expenses = []


def add_expense():
    category = input("Enter category: ")

    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            break

        except ValueError:
            print("Please enter a valid numeric amount.")

    description = input("Enter description: ")

    expense = {
        "category": category,
        "amount": amount,
        "description": description
    }

    expenses.append(expense)
    print("Expense added successfully.")


def view_expenses():
    if len(expenses) == 0:
        print("No expenses found.")
        return

    print("\n===== EXPENSES =====")
    for index, expense in enumerate(expenses):
        print(
            f"{index + 1}. {expense['category']} - "
            f"₹{expense['amount']} - {expense['description']}"
        )


def calculate_total():
    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    print(f"Total expenses: ₹{total}")


def filter_by_category():
    category = input("Enter category to filter: ")

    print(f"\nExpenses in category: {category}")

    found = False

    for expense in expenses:
        if expense["category"].strip().lower() == category.strip().lower():
            print(
                f"{expense['category']} - "
                f"₹{expense['amount']} - {expense['description']}"
            )
            found = True

    if found == False:
        print("No expenses found for this category.")


def save_expenses():
    with open("expenses.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(["category", "amount", "description"])

        for expense in expenses:
            writer.writerow([
                expense["category"],
                expense["amount"],
                expense["description"]
            ])

    print("Expenses saved successfully.")


def load_expenses():
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.DictReader(file)

            expenses.clear()

            for row in reader:
                expenses.append(row)

        print("Expenses loaded successfully.")

    except FileNotFoundError:
        print("No saved expenses file found.")


def main():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Calculate Total")
        print("4. Filter by Category")
        print("5. Save Expenses")
        print("6. Load Expenses")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            calculate_total()
        elif choice == "4":
            filter_by_category()
        elif choice == "5":
            save_expenses()
        elif choice == "6":
            load_expenses()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
