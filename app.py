
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# PAGE SETTINGS
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# DATABASE CONNECTION
conn = sqlite3.connect("expense.db")

cursor = conn.cursor()

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()

# WEBSITE TITLE
st.title("💰 Expense Tracker Website")


# SIDEBAR MENU
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Expense",
        "View Expenses",
        "Analytics",
        "Delete Expense"
    ]
)

# ADD EXPENSE
if menu == "Add Expense":

    st.header("➕ Add New Expense")

    title = st.text_input(
        "Expense Title"
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    date = st.date_input(
        "Select Date"
    )

    if st.button("Add Expense"):

        cursor.execute("""
        INSERT INTO expenses
        (title, amount, category, date)
        VALUES (?, ?, ?, ?)
        """, (
            title,
            amount,
            category,
            str(date)
        ))

        conn.commit()

        st.success(
            "Expense Added Successfully!"
        )

# VIEW EXPENSES
elif menu == "View Expenses":

    st.header("📋 All Expenses")

    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    st.dataframe(df)

# ANALYTICS
elif menu == "Analytics":

    st.header("📊 Expense Analytics")

    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    if len(df) == 0:

        st.warning(
            "No expense data available!"
        )

    else:

        # CALCULATIONS
        total = df["amount"].sum()

        average = df["amount"].mean()

        maximum = df["amount"].max()

        # DASHBOARD CARDS
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Expense",
            f"₹ {total}"
        )

        col2.metric(
            "Average Expense",
            f"₹ {average:.2f}"
        )

        col3.metric(
            "Highest Expense",
            f"₹ {maximum}"
        )

        # CATEGORY ANALYSIS
        category_data = df.groupby(
            "category"
        )["amount"].sum()

        # PIE CHART
        fig, ax = plt.subplots()

        ax.pie(
            category_data,
            labels=category_data.index,
            autopct='%1.1f%%'
        )

        ax.set_title(
            "Expense Category Distribution"
        )

        st.pyplot(fig)

# DELETE EXPENSE
elif menu == "Delete Expense":

    st.header("🗑 Delete Expense")

    # Load all expenses
    df = pd.read_sql_query(
        "SELECT * FROM expenses",
        conn
    )

    # Show expenses table
    st.dataframe(df)

    # Take expense ID
    expense_id = st.number_input(
        "Enter Expense ID to Delete",
        min_value=1,
        step=1
    )

    # Delete button
    if st.button("Delete Expense"):

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        conn.commit()

        st.success(
            "Expense Deleted Successfully!"
        )

        conn.close()
        