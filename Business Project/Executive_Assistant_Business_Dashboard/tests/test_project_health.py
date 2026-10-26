from pathlib import Path

import pandas as pd

from utils.charts import expense_department_chart, meeting_status_chart, task_status_chart
from utils.data_loader import load_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_required_workbooks_exist():
    expected = {"meetings.xlsx", "tasks.xlsx", "followups.xlsx", "vendors.xlsx", "expenses.xlsx", "calendar.xlsx"}
    actual = {path.name for path in (PROJECT_ROOT / "data").glob("*.xlsx")}
    assert expected <= actual


def test_load_data_returns_expected_tables():
    data = load_data()
    assert set(data) == {"meetings", "tasks", "followups", "vendors", "expenses", "calendar"}
    assert all(isinstance(frame, pd.DataFrame) for frame in data.values())
    assert not data["meetings"].empty
    assert {"Status"} <= set(data["meetings"].columns)
    assert {"Status"} <= set(data["tasks"].columns)
    assert {"Department", "Amount"} <= set(data["expenses"].columns)


def test_charts_build_from_small_sample_data():
    meetings = pd.DataFrame({"Status": ["Completed", "Pending", "Completed"]})
    tasks = pd.DataFrame({"Status": ["Completed", "Pending", "Pending"]})
    expenses = pd.DataFrame({"Department": ["Sales", "Ops", "Sales"], "Amount": [100, 50, 25]})
    meeting_fig = meeting_status_chart(meetings)
    task_fig = task_status_chart(tasks)
    expense_fig = expense_department_chart(expenses)
    assert meeting_fig.data and task_fig.data and expense_fig.data
    assert meeting_fig.layout.title.text == "Meeting Status"
    assert task_fig.layout.title.text == "Task Status"
    assert expense_fig.layout.title.text == "Expense by Department"
