# Week 2 Python Debugging Log

## 1. Project Overview

### Project Name

Python Expense Tracker

### Objective

The objective of this debugging exercise was to identify, reproduce,
investigate, fix, and verify bugs in a command-line Python expense
tracking application.

The application provides the following functionality:

- Add expenses
- View expenses
- Calculate total expenses
- Filter expenses by category
- Save expenses to a CSV file
- Load expenses from a CSV file
- Validate user input
- Handle file-related errors

### Debugging Scenario Note

The original debugging script referenced in the internship task was not
available through the provided internship resources at the time of
implementation.

Therefore, a self-created Python Expense Tracker application was used
as the debugging scenario.

The project contains both the original buggy implementation and the
corrected implementation so that the debugging process can be clearly
demonstrated.

The original implementation is preserved as:

`buggy_expense_tracker.py`

The corrected implementation is:

`corrected_expense_tracker.py`

---

# 2. Project Structure

```text
week2-python-debugging/
│
├── buggy_expense_tracker.py
├── corrected_expense_tracker.py
├── expenses.csv
├── debugging_log.md
└── tests/
    └── test_expense_tracker.py
```

### File Description

| File | Purpose |
|---|---|
| `buggy_expense_tracker.py` | Original buggy implementation |
| `corrected_expense_tracker.py` | Corrected implementation |
| `expenses.csv` | CSV file used for expense storage |
| `debugging_log.md` | Debugging and troubleshooting documentation |
| `tests/test_expense_tracker.py` | Automated pytest test cases |

---

# 3. Baseline Testing

The original `buggy_expense_tracker.py` was executed before applying
any fixes.

The application was manually tested to identify reproducible problems.

Five bugs were identified:

1. Amount values were stored as strings, causing a `TypeError` during
   total calculation.
2. Category filtering was case-sensitive.
3. Loading a missing CSV file caused a `FileNotFoundError`.
4. Invalid expense amounts such as text, zero, and negative values were
   accepted.
5. Loading the CSV file multiple times created duplicate expense records.

Each issue was reproduced and investigated before applying the
corresponding fix.

---

# 4. Bug 1 - Amount Stored as String

## 4.1 Problem

The application collected the expense amount using:

```python
amount = input("Enter amount: ")
```

Python's `input()` function returns a string.

The application later attempted to calculate the total using:

```python
total = total + expense["amount"]
```

This caused the application to attempt to add an integer and a string.

---

## 4.2 Reproduction

Two expenses were entered:

```text
Food - 200
Transport - 100
```

When the Calculate Total option was selected, the application produced:

```text
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

The type of the amount was also verified separately:

```python
amount = input("Enter amount: ")
print(type(amount))
```

The result was:

```text
<class 'str'>
```

This confirmed that the amount was being stored as a string.

---

## 4.3 Root Cause

The root cause was that the value returned by `input()` was stored
directly without converting it to a numeric type.

The total calculation expected numeric values but received strings.

---

## 4.4 Fix Applied

The amount input was converted to a floating-point number using
`float()`.

A `try-except` block was also added to handle invalid numeric input.

The amount was additionally checked to ensure that it was greater than
zero.

Corrected logic:

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
```

---

## 4.5 Verification

Two valid expenses were added:

```text
Food - ₹200.0
Transport - ₹100.0
```

The Calculate Total option produced:

```text
Total expenses: ₹300.0
```

The calculation completed without a `TypeError`.

---

## 4.6 Result

**PASS**

The application now converts valid amount input into numeric values
before performing calculations.

---

# 5. Bug 2 - Case-Sensitive Category Filtering

## 5.1 Problem

The original category filtering logic used exact string comparison:

```python
if expense["category"] == category:
```

This caused category filtering to be case-sensitive.

For example:

```text
Food
food
FOOD
```

were treated as different values.

---

## 5.2 Reproduction

An expense was added using the category:

```text
Food
```

The filtering operation was then performed using:

```text
food
```

The application did not return the `Food` expense.

The behavior was also verified with a direct comparison:

```python
print("Food" == "food")
```

which returned:

```text
False
```

---

## 5.3 Root Cause

The root cause was exact string comparison without normalizing the
category values.

---

## 5.4 Fix Applied

The comparison was changed to:

```python
if expense["category"].strip().lower() == category.strip().lower():
```

The `strip()` method removes leading and trailing whitespace.

The `lower()` method makes the comparison case-insensitive.

---

## 5.5 Verification

The following category inputs were tested:

```text
food
FOOD
foOd
```

All three correctly matched the stored category:

```text
Food
```

Multiple expenses in the same category were also displayed correctly.

For example:

```text
Food - ₹200.0 - Lunch
Food - ₹300.0 - Lunch
```

---

## 5.6 Result

**PASS**

Category filtering now works regardless of letter case and ignores
unnecessary leading or trailing spaces.

---

# 6. Bug 3 - Missing CSV File Handling

## 6.1 Problem

The original application attempted to open the CSV file directly:

```python
with open("expenses.csv", "r") as file:
    reader = csv.DictReader(file)
```

If the file did not exist, the application terminated with a
`FileNotFoundError`.

---

## 6.2 Reproduction

The application was executed without an existing `expenses.csv` file.

The Load Expenses option was selected.

The original application produced:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'expenses.csv'
```

---

## 6.3 Root Cause

The `load_expenses()` function assumed that the CSV file would always
exist.

There was no exception handling for a missing file.

---

## 6.4 Fix Applied

The file-loading operation was placed inside a `try-except` block.

Corrected implementation:

```python
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
```

---

## 6.5 Verification - Missing File

The application was started without `expenses.csv`.

The Load Expenses option was selected.

The corrected application displayed:

```text
No saved expenses file found.
```

The application continued running instead of crashing.

---

## 6.6 Verification - Existing File

An expense was added and saved using the Save Expenses option.

The application displayed:

```text
Expenses saved successfully.
```

The Load Expenses option was then selected.

The application displayed:

```text
Expenses loaded successfully.
```

This confirmed that the fix did not prevent normal CSV loading.

---

## 6.7 Result

**PASS**

The application now handles a missing CSV file gracefully while still
supporting normal loading when the file exists.

---

# 7. Bug 4 - Invalid Amount Validation

## 7.1 Problem

The original application accepted the expense amount using:

```python
amount = input("Enter amount: ")
```

There was no validation to ensure that the entered value was a valid
positive number.

---

## 7.2 Reproduction

The original application accepted invalid input such as:

```text
abc
```

without rejecting it.

Further investigation showed that simply converting the value using
`float()` would still allow values such as:

```text
0
-100
```

Therefore, both numeric conversion and positive-value validation were
required.

---

## 7.3 Root Cause

The root cause was the absence of:

1. Numeric conversion
2. Invalid input handling
3. Positive-value validation

---

## 7.4 Fix Applied

The amount is now converted to `float` and checked to ensure that it
is greater than zero.

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
```

---

## 7.5 Verification

The following inputs were tested:

| Input | Expected Behavior | Result |
|---|---|---|
| `abc` | Reject | PASS |
| `0` | Reject | PASS |
| `-100` | Reject | PASS |
| `150.50` | Accept | PASS |

The valid input:

```text
150.50
```

was accepted successfully.

The application displayed:

```text
Expense added successfully.
```

---

## 7.6 Result

**PASS**

Invalid and non-positive amounts are rejected, while valid positive
numeric amounts are accepted.

---

# 8. Bug 5 - Duplicate Records When Loading

## 8.1 Problem

Loading the CSV file multiple times caused duplicate expense records.

---

## 8.2 Reproduction

Two expenses were added:

```text
1. Food - ₹200.0 - Lunch
2. Travel - ₹100.0 - Bus
```

The expenses were saved to `expenses.csv`.

Before loading, the application displayed:

```text
===== EXPENSES =====
1. Food - ₹200.0 - Lunch
2. Travel - ₹100.0 - Bus
```

The CSV file was then loaded.

After one load, the original application displayed:

```text
===== EXPENSES =====
1. Food - ₹200.0 - Lunch
2. Travel - ₹100.0 - Bus
3. Food - ₹200.0 - Lunch
4. Travel - ₹100.0 - Bus
```

The two records had been duplicated.

---

## 8.3 Root Cause

The original implementation directly appended every CSV record to the
existing `expenses` list:

```python
for row in reader:
    expenses.append(row)
```

The existing in-memory records were not removed before loading.

---

## 8.4 Fix Applied

The existing records are cleared before loading the CSV records:

```python
expenses.clear()

for row in reader:
    expenses.append(row)
```

The complete corrected loading function is:

```python
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
```

---

## 8.5 Verification

The corrected application was tested by loading the same CSV file
multiple times.

After the first load:

```text
===== EXPENSES =====
1. Food - ₹200.0 - Lunch
2. Travel - ₹100.0 - Bus
```

The same CSV file was loaded again.

After the second load:

```text
===== EXPENSES =====
1. Food - ₹200.0 - Lunch
2. Travel - ₹100.0 - Bus
```

The number of records remained two.

No duplicate records were created.

---

## 8.6 Result

**PASS**

Repeated CSV loading no longer creates duplicate expense records.

---

# 9. Automated Testing

After completing the manual debugging and verification process,
automated tests were added using `pytest`.

## 9.1 Test File

```text
tests/test_expense_tracker.py
```

The test suite contains six automated tests.

---

## 9.2 Test Cases

### Test 1 - Valid Amount

```text
test_add_expense_valid_amount
```

Verifies that a valid positive numeric amount is accepted and stored
correctly.

**Result: PASS**

---

### Test 2 - Invalid Amount Rejection

```text
test_add_expense_rejects_invalid_amount
```

Verifies that invalid input such as:

```text
abc
0
-100
```

is rejected before a valid amount is accepted.

**Result: PASS**

---

### Test 3 - Case-Insensitive Category Filtering

```text
test_filter_category_is_case_insensitive
```

Verifies that a stored category such as `Food` can be found using
different letter cases such as `food`.

**Result: PASS**

---

### Test 4 - Missing CSV File

```text
test_load_missing_file
```

Verifies that attempting to load a missing CSV file does not crash
the application and produces the expected message.

**Result: PASS**

---

### Test 5 - Duplicate-Free CSV Loading

```text
test_load_does_not_duplicate_records
```

Verifies that loading the same CSV file multiple times does not
increase the number of in-memory records.

**Result: PASS**

---

### Test 6 - Total Calculation

```text
test_calculate_total
```

Verifies that the total of multiple expense amounts is calculated
correctly.

**Result: PASS**

---

# 10. Automated Test Execution

The test suite was executed using:

```powershell
python -m pytest -v
```

Environment:

```text
Platform: Windows
Python: 3.14.7
pytest: 9.1.1
pluggy: 1.6.0
```

The test suite collected:

```text
6 items
```

All six tests passed:

```text
tests/test_expense_tracker.py::test_add_expense_valid_amount PASSED
tests/test_expense_tracker.py::test_add_expense_rejects_invalid_amount PASSED
tests/test_expense_tracker.py::test_filter_category_is_case_insensitive PASSED
tests/test_expense_tracker.py::test_load_missing_file PASSED
tests/test_expense_tracker.py::test_load_does_not_duplicate_records PASSED
tests/test_expense_tracker.py::test_calculate_total PASSED
```

Final result:

```text
6 passed in 0.22s
```

---

# 11. Final Debugging Summary

All five identified bugs were:

- Reproduced
- Investigated
- Traced to their root causes
- Fixed
- Manually verified
- Covered by automated tests where applicable

## Final Results

| Bug | Description | Status |
|---|---|---|
| Bug 1 | Amount stored as string | PASS |
| Bug 2 | Case-sensitive category filtering | PASS |
| Bug 3 | Missing CSV file handling | PASS |
| Bug 4 | Invalid amount validation | PASS |
| Bug 5 | Duplicate records during loading | PASS |

Automated testing also confirmed that the corrected implementation
passed all six test cases.

```text
6 passed in 0.22s
```

---

# 12. Final Application Behavior

After debugging, the application correctly supports:

- Adding valid expenses
- Rejecting non-numeric amounts
- Rejecting zero amounts
- Rejecting negative amounts
- Viewing stored expenses
- Calculating expense totals
- Case-insensitive category filtering
- Saving expenses to CSV
- Loading expenses from CSV
- Handling a missing CSV file without crashing
- Preventing duplicate records during repeated CSV loading

---

# 13. Final Project Files

The completed project contains:

```text
week2-python-debugging/
│
├── buggy_expense_tracker.py
├── corrected_expense_tracker.py
├── expenses.csv
├── debugging_log.md
│
└── tests/
    └── test_expense_tracker.py
```

The original buggy implementation was retained separately so that the
debugging process can be compared with the corrected implementation.

---

# 14. Conclusion

The debugging exercise demonstrated a complete Python debugging
workflow:

1. Execute the original application.
2. Reproduce the observed bugs.
3. Investigate the program behavior.
4. Identify the root cause of each issue.
5. Apply targeted fixes.
6. Manually verify each fix.
7. Create automated tests.
8. Execute the automated test suite.
9. Confirm that all automated tests pass.

The final corrected application successfully passed the manual
verification process and all six automated tests.
