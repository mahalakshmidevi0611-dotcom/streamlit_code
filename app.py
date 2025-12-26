import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expenses Dashboard", layout="wide")

st.sidebar.title("☰ Menu")
menu = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Add Expense", "Summary"]
)


if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Category", "Amount"]
    )

df = st.session_state.data

if menu == "Dashboard":
    st.title("💸 Daily Expenses Dashboard")

    if df.empty:
        st.warning("No expenses added yet")
    else:
        col1, col2 = st.columns(2)

        total = df["Amount"].sum()
        col1.metric("💰 Total Spending", f"₹ {total}")

        today = df[df["Date"] == pd.to_datetime("today").normalize()]
        col2.metric("📅 Today Spending", f"₹ {today['Amount'].sum()}")

        st.subheader("📋 Expense Details")
        st.dataframe(df, use_container_width=True)

        category_sum = df.groupby("Category")["Amount"].sum()

        st.subheader("📊 Category-wise Spending")
        st.bar_chart(category_sum)

elif menu == "Add Expense":
    st.title("➕ Add New Expense")

    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox(
            "Category",
            ["Food", "Travel", "Shopping"]
        )
        amount = st.number_input("Amount", min_value=0)

        submit = st.form_submit_button("Add Expense")

    if submit:
        new_row = {
            "Date": pd.to_datetime(date),
            "Category": category,
            "Amount": amount
        }
        st.session_state.data = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Expense Added Successfully ✅")


elif menu == "Summary":
    st.title("📈 Expense Summary")

    if df.empty:
        st.info("Add expenses to see summary")
    else:
        category_sum = df.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()
        ax.pie(
            category_sum,
            labels=category_sum.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Expense Distribution")
        st.pyplot(fig)

        st.subheader("Category Summary")
        st.table(category_sum.reset_index())
