import streamlit as st

st.set_page_config(page_title="TACSiS Enhanced", layout="centered")
st.title("💰 TACSiS – Income & Expense Tracker")

# Initialize session states
if "job_count" not in st.session_state:
    st.session_state.job_count = 2
if "expense_count" not in st.session_state:
    st.session_state.expense_count = 5
if "total_income" not in st.session_state:
    st.session_state.total_income = 0
if "total_expense" not in st.session_state:
    st.session_state.total_expense = 0

# ------------------- INCOME SECTION ------------------- #
st.markdown("## Income Sources")

income_inputs = []
with st.form("income_form"):
    for i in range(st.session_state.job_count):
        col1, col2 = st.columns([2, 1])
        with col1:
            label = st.text_input(f"Job {i+1} Title", value=f"Job {i+1}", key=f"title_{i}")
        with col2:
            amount = st.number_input(f"Amount", min_value=0.0, step=100.0, key=f"amt_{i}")
        income_inputs.append((label, amount))

    add_job = st.form_submit_button("➕ Add Another Job")
    submit_income = st.form_submit_button("✅ Done Submitting Income")

if add_job:
    st.session_state.job_count += 1

if submit_income:
    st.session_state.total_income = sum(x[1] for x in income_inputs)
    st.success(f"💼 Total Monthly Income: ${st.session_state.total_income:,.2f}")

# ------------------- EXPENSE SECTION ------------------- #
st.markdown("---")
st.markdown("## Expenses")

default_expenses = ["Rent/Mortgage", "Internet", "Groceries", "Phone", "Subscriptions"]
expense_inputs = []

with st.form("expense_form"):
    for i in range(st.session_state.expense_count):
        col1, col2 = st.columns([2, 1])
        with col1:
            label = st.text_input(f"Expense Category {i+1}", 
                                  value=default_expenses[i] if i < len(default_expenses) else "", 
                                  key=f"exp_cat_{i}")
        with col2:
            amount = st.number_input(f"Amount", min_value=0.0, step=50.0, key=f"exp_amt_{i}")
        expense_inputs.append((label, amount))

    add_exp = st.form_submit_button("➕ Add Another Expense")
    submit_exp = st.form_submit_button("✅ Done Submitting Expenses")

if add_exp:
    st.session_state.expense_count += 1

if submit_exp:
    st.session_state.total_expense = sum(x[1] for x in expense_inputs)
    st.success(f"💸 Total Monthly Expenses: ${st.session_state.total_expense:,.2f}")

# ------------------- REMAINING BALANCE ------------------- #
if st.session_state.total_income and st.session_state.total_expense:
    net_balance = st.session_state.total_income - st.session_state.total_expense
    st.markdown("---")
    st.subheader("📊 Net Monthly Balance")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("💼 Total Income", f"${st.session_state.total_income:,.2f}", disabled=True)
    with col2:
        st.text_input("💸 Total Expenses", f"${st.session_state.total_expense:,.2f}", disabled=True)
    with col3:
        st.text_input("🧾 Remaining Balance After Expenses", f"${net_balance:,.2f}", disabled=True)
