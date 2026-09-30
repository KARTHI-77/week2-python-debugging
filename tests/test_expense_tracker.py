import importlib.util
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
MODULE_PATH = PROJECT_DIR / "corrected_expense_tracker.py"


spec = importlib.util.spec_from_file_location(
    "expense_tracker",
    MODULE_PATH
)
expense_tracker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(expense_tracker)


def reset_expenses():
    expense_tracker.expenses.clear()


def test_add_expense_valid_amount(monkeypatch):
    reset_expenses()

    inputs = iter(["Food", "150.50", "Groceries"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    expense_tracker.add_expense()

    assert len(expense_tracker.expenses) == 1
    assert expense_tracker.expenses[0]["category"] == "Food"
    assert expense_tracker.expenses[0]["amount"] == 150.50
    assert expense_tracker.expenses[0]["description"] == "Groceries"


def test_add_expense_rejects_invalid_amount(monkeypatch):
    reset_expenses()

    inputs = iter(["Food", "abc", "0", "-100", "200", "Lunch"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    expense_tracker.add_expense()

    assert len(expense_tracker.expenses) == 1
    assert expense_tracker.expenses[0]["amount"] == 200.0


def test_filter_category_is_case_insensitive(monkeypatch, capsys):
    reset_expenses()

    expense_tracker.expenses.append({
        "category": "Food",
        "amount": 200.0,
        "description": "Lunch"
    })

    inputs = iter(["food"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    expense_tracker.filter_by_category()

    output = capsys.readouterr().out

    assert "Food - ₹200.0 - Lunch" in output


def test_load_missing_file(monkeypatch, capsys, tmp_path):
    reset_expenses()

    monkeypatch.chdir(tmp_path)

    expense_tracker.load_expenses()

    output = capsys.readouterr().out

    assert "No saved expenses file found." in output
    assert expense_tracker.expenses == []


def test_load_does_not_duplicate_records(monkeypatch, tmp_path):
    reset_expenses()

    csv_file = tmp_path / "expenses.csv"
    csv_file.write_text(
        "category,amount,description\n"
        "Food,200,Lunch\n"
        "Travel,100,Bus\n"
    )

    monkeypatch.chdir(tmp_path)

    expense_tracker.load_expenses()

    assert len(expense_tracker.expenses) == 2

    expense_tracker.load_expenses()

    assert len(expense_tracker.expenses) == 2


def test_calculate_total(capsys):
    reset_expenses()

    expense_tracker.expenses.extend([
        {
            "category": "Food",
            "amount": 200.0,
            "description": "Lunch"
        },
        {
            "category": "Travel",
            "amount": 100.0,
            "description": "Bus"
        }
    ])

    expense_tracker.calculate_total()

    output = capsys.readouterr().out

    assert "Total expenses: ₹300.0" in output