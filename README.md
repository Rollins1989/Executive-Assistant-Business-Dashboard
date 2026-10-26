# Executive Assistant Business Intelligence Dashboard

A Python + Streamlit dashboard for executive operations and business reporting. It brings together meetings, tasks, follow-ups, vendors, expenses, calendar activity and management information summaries.

## Project highlights

- Multi-page Streamlit dashboard with KPI cards and Plotly visualizations
- Excel-backed sample datasets and downloadable report exports
- Meeting, task, follow-up, vendor, expense and calendar views
- Basic automated tests plus GitHub Actions checks

## Preview

The application folder contains exported chart previews. These are analytics images rather than full-window screenshots of the running app.

![Meeting status preview](Business%20Project/Executive_Assistant_Business_Dashboard/charts/Meeting_Status_MIS.png)

![Task status preview](Business%20Project/Executive_Assistant_Business_Dashboard/charts/Task_Status.png)

![Expense by department preview](Business%20Project/Executive_Assistant_Business_Dashboard/charts/Department_Expense.png)

## Run locally

Open a terminal in `Business Project/Executive_Assistant_Business_Dashboard`:

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Run tests

From the same directory:

```bash
python -m pytest -q
```

GitHub Actions is configured to run the checks when relevant project files change.

## Live demo

**Live Streamlit URL: not deployed yet.** To publish it, create an app in Streamlit Community Cloud, choose this repository and the `main` branch, and set the main file path to:

`Business Project/Executive_Assistant_Business_Dashboard/streamlit_app.py`

After the deployment succeeds, replace this note with the generated public `*.streamlit.app` link. A live link should not be advertised before the app has actually been deployed and verified.

## Tech stack

Python · Streamlit · Pandas · NumPy · Plotly · Excel/OpenPyXL · pytest
