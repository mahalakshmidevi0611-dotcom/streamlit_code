import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expenses Dashboard", layout="wide")


st.sidebar.title("☰ Menu")
menu = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Add Expense",
        "Expense History",
        "Category Insights",
        "Budget Tracker",
        "Summary",
        "Download Data",
        "About App"
    ]
)

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Category", "Amount"]
    )

if "budget" not in st.session_state:
    st.session_state.budget = 0

df = st.session_state.data


if menu == "Dashboard":
    st.title(" Daily Expenses Dashboard")

    if df.empty:
        st.warning("No expenses added yet")
    else:
        col1, col2 = st.columns(2)

        total = df["Amount"].sum()
        col1.metric(" Total Spending", f"₹ {total}")

        today = df[df["Date"] == pd.to_datetime("today").normalize()]
        col2.metric("Today Spending", f"₹ {today['Amount'].sum()}")

        st.subheader("Expense Details")
        st.dataframe(df, use_container_width=True)

        st.subheader("Category-wise Spending")
        st.bar_chart(df.groupby("Category")["Amount"].sum())


elif menu == "Add Expense":
    st.title("➕ Add New Expense")

    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Travel", "Shopping"])
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


elif menu == "Expense History":
    st.title(" Expense History")

    if df.empty:
        st.info("No data available")
    else:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + df["Category"].unique().tolist()
        )

        if category_filter != "All":
            df = df[df["Category"] == category_filter]

        st.dataframe(df.sort_values("Date"), use_container_width=True)

elif menu == "Category Insights":
    st.title(" Category Insights")

    if df.empty:
        st.info("Add expenses to see insights")
    else:
        category_sum = df.groupby("Category")["Amount"].sum()

        st.metric(
            "Highest Spending Category",
            category_sum.idxmax(),
            f"₹ {category_sum.max()}"
        )

        st.metric(
            "Lowest Spending Category",
            category_sum.idxmin(),
            f"₹ {category_sum.min()}"
        )

        st.bar_chart(category_sum)


elif menu == "Budget Tracker":
    st.title(" Budget Tracker")

    budget = st.number_input(
        "Set Monthly Budget (₹)",
        min_value=0,
        value=st.session_state.budget
    )

    st.session_state.budget = budget

    total_spent = df["Amount"].sum()

    st.metric("Total Spent", f"₹ {total_spent}")
    st.metric("Remaining Budget", f"₹ {budget - total_spent}")

    if total_spent > budget and budget > 0:
        st.error("⚠ Budget Exceeded!")

elif menu == "Summary":
    st.title(" Expense Summary")

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

        st.table(category_sum.reset_index())


elif menu == "Download Data":
    st.title("⬇ Download Expense Data")

    if df.empty:
        st.info("No data to download")
    else:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="expenses_data.csv",
            mime="text/csv"
        )

elif menu == "About App":
    st.title("ℹ About This App")

    st.markdown("""
    ### 💸 Daily Expenses Dashboard

    This is an interactive dashboard built using **Streamlit** to track and analyze daily expenses.

    **Features:**
    - Expense tracking
    - Category insights
    - Budget monitoring
    - Data visualization
    - CSV download

    **Tech Stack:**
    - Python
    - Streamlit
    - Pandas
    - Matplotlib

    **Developed by:**  
    **Maha Lakshmi**
    """)
