# Week 2 Python Debugging Log

## Baseline Testing

## Root Cause Investigation - Bug 1

### Investigation

The traceback indicated that the application attempted to add
an integer and a string:

`TypeError: unsupported operand type(s) for +: 'int' and 'str'`

The value flow was traced from `add_expense()` to
`calculate_total()`.

The amount is collected using:

```python
amount = input("Enter amount: ")

## Fix - Bug 1: Amount Stored as String

### Original Problem

The application stored the amount returned by `input()` as a
string. This caused a TypeError when the application attempted
to add the amount to the numeric total.

### Fix Applied

The amount input was converted to a floating-point number using
`float()` and protected with `try/except` to handle invalid
numeric input.

The application also validates that the amount is greater than
zero.

### Corrected Logic

```python
while True:
    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            continue

        break

    except ValueError:
        print("Please enter a valid numeric amount.")

### Root Cause Investigation - Bug 2

The category filtering logic compares the stored category and
the user's input using exact string equality:

```python
if expense["category"] == category:

---

### Root Cause Investigation - Bug 3

The application failed when the `expenses.csv` file was not
present in the working directory.

The relevant code is:

```python
with open("expenses.csv", "r") as file:
    reader = csv.DictReader(file)

---

### Root Cause Investigation - Bug 4

The application accepts the expense amount using:

```python
amount = input("Enter amount: ")

---

### Root Cause Investigation - Bug 5

The application was tested by adding two expenses, saving them
to `expenses.csv`, and then loading the file multiple times.

Initial state:

```text
1. Food - ₹200 - Lunch
2. Transport - ₹100 - bus