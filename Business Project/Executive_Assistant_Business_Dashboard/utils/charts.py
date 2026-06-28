import plotly.express as px


def meeting_status_chart(df):

    fig = px.pie(

        df,

        names="Status",

        title="Meeting Status"

    )

    fig.update_layout(

        template="plotly_white",

        height=400

    )

    return fig



def task_status_chart(df):

    fig = px.bar(

        df["Status"].value_counts().reset_index(),

        x="Status",

        y="count",

        title="Task Status"

    )

    fig.update_layout(

        template="plotly_white",

        height=400

    )

    return fig



def expense_department_chart(df):

    summary = (

        df.groupby("Department")["Amount"]

        .sum()

        .reset_index()

    )

    fig = px.bar(

        summary,

        x="Department",

        y="Amount",

        title="Expense by Department"

    )

    fig.update_layout(

        template="plotly_white",

        height=400

    )

    return fig