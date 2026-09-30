# Python Expense Tracker - Week 2 Debugging

A command-line Python Expense Tracker created as a debugging and troubleshooting exercise.

## Project Overview

This project demonstrates a complete Python debugging workflow:

- Reproducing software bugs
- Investigating root causes
- Applying targeted fixes
- Performing manual verification
- Writing automated tests using pytest

> **Note:** The original debugging script referenced in the internship task was not available through the provided resources at the time of implementation. Therefore, a self-created Python Expense Tracker was used as the debugging scenario.

## Features

The application supports:

- Add expenses
- View expenses
- Calculate total expenses
- Filter expenses by category
- Save expenses to CSV
- Load expenses from CSV
- Validate expense amounts
- Handle missing CSV files

## Project Structure

```text
week2-python-debugging/
│
├── buggy_expense_tracker.py
├── corrected_expense_tracker.py
├── expenses.csv
├── debugging_log.md
├── README.md
│
└── tests/
    └── test_expense_tracker.py
```

## Bugs Identified and Fixed

### 1. Amount Stored as String

**Problem:**  
The `input()` function returned the expense amount as a string, causing a `TypeError` during total calculation.

**Fix:**  
Converted the input to `float` and added validation.

---

### 2. Case-Sensitive Category Filtering

**Problem:**  
`Food`, `food`, and `FOOD` were treated as different categories.

**Fix:**  
Used `strip()` and `lower()` for case-insensitive comparison.

```python
if expense["category"].strip().lower() == category.strip().lower():
```

---

### 3. Missing CSV File

**Problem:**  
Loading a non-existent `expenses.csv` caused a `FileNotFoundError`.

**Fix:**  
Added `try-except` handling for `FileNotFoundError`.

---

### 4. Invalid Expense Amount

**Problem:**  
The original application accepted non-numeric, zero, and negative amounts.

**Fix:**  
Added numeric conversion and positive-value validation.

```python
amount = float(input("Enter amount: "))

if amount <= 0:
    print("Amount must be greater than zero.")
```

---

### 5. Duplicate Records During Loading

**Problem:**  
Loading the CSV multiple times appended duplicate records to the existing list.

**Fix:**  
Cleared the existing records before loading:

```python
expenses.clear()
```

## Testing

Automated tests were created using `pytest`.

Run the tests with:

```powershell
python -m pytest -v
```

### Test Results

```text
6 passed in 0.22s
```

The test suite verifies:

- Valid amount handling
- Invalid amount rejection
- Case-insensitive category filtering
- Missing CSV file handling
- Duplicate-free CSV loading
- Total calculation

## Manual Verification

All five identified bugs were manually reproduced and verified after their fixes.

The corrected application successfully handled:

- Valid expense amounts
- Invalid input
- Category filtering
- CSV saving
- CSV loading
- Missing CSV files
- Repeated CSV loading without duplication
- Total calculation

## Documentation

Detailed debugging information is available in:

```text
debugging_log.md
```

The debugging log contains:

- Baseline testing
- Bug reproduction
- Root cause investigation
- Fixes applied
- Manual verification
- Automated testing results

## Technologies Used

- Python 3.14
- CSV
- pytest
- Git
- GitHub

## Conclusion

This project demonstrates a structured approach to debugging a Python application by reproducing problems, identifying their root causes, implementing fixes, and validating the corrected behavior through manual and automated testing.
