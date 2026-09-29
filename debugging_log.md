# Week 2 Python Debugging Log

## Baseline Testing

### Bug 1 - Amount Stored as String

**Steps to reproduce:**
1. Start the application.
2. Add Food expense with amount 200.
3. Add Transport expense with amount 100.
4. Select Calculate Total.

**Expected behavior:**
The application should calculate the total as ₹300.

**Actual behavior:**
The application terminated with a TypeError.

**Observed error:**
TypeError: unsupported operand type(s) for +: 'int' and 'str'

**Traceback location:**
`calculate_total()` - line 38.

**Status:**
Reproduced. Root cause investigation pending.

---

### Bug 2 - Case-Sensitive Category Filtering

**Steps to reproduce:**
1. Add an expense with category `Food`.
2. Select Filter by Category.
3. Enter `food`.

**Expected behavior:**
The Food expense should be displayed.

**Actual behavior:**
`No expenses found for this category.`

**Status:**
Reproduced. Root cause investigation pending.

---

### Bug 3 - Missing CSV File

**Steps to reproduce:**
1. Ensure `expenses.csv` does not exist.
2. Start the application.
3. Select Load Expenses.

**Expected behavior:**
The application should handle the missing file gracefully.

**Actual behavior:**
The application terminated with `FileNotFoundError`.

**Status:**
Reproduced. Root cause investigation pending.

---

### Bug 4 - Invalid Amount Accepted

**Steps to reproduce:**
1. Select Add Expense.
2. Enter category `Food`.
3. Enter amount `abc`.
4. Enter a description.

**Expected behavior:**
The application should reject non-numeric expense amounts.

**Actual behavior:**
The application accepted `abc` and displayed `Expense added successfully.`

**Status:**
Reproduced. Root cause investigation pending.

---

### Bug 5 - Duplicate Records During Loading

**Steps to reproduce:**
1. Save expenses to `expenses.csv`.
2. Select Load Expenses.
3. Select Load Expenses again.

**Expected behavior:**
Loading the saved file should not create duplicate records.

**Actual behavior:**
Records are appended to the existing list each time the file is loaded.

**Status:**
Reproduced. Root cause investigation pending.