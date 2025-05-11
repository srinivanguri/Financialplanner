import streamlit as st

st.set_page_config(page_title="TACSiS Financial Planner", layout="centered")
st.title("💼 TACSiS – AI-Powered Financial Planner")

tabs = st.tabs([
    "💰 Income & Expenses",
    "💳 Credit Cards",
    "📊 Mortgage Readiness"
])

# ----------- INIT STATE ----------- #
for key, default in {
    "job_count": 2,
    "expense_count": 5,
    "card_count": 1,
    "total_income": 0,
    "total_expense": 0,
    "total_min_pay": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ----------- TAB 1: Income & Expenses ----------- #
with tabs[0]:
    st.subheader("💰 Income Sources")
    income_inputs = []
    with st.form("income_form"):
        for i in range(st.session_state.job_count):
            col1, col2 = st.columns([2, 1])
            with col1:
                label = st.text_input(f"Job {i+1} Title", value=f"Job {i+1}", key=f"title_{i}")
            with col2:
                amount = st.number_input(f"Amount", min_value=0.0, step=100.0, key=f"amt_{i}")
            income_inputs.append((label, amount))
        if st.form_submit_button("➕ Add Another Job"):
            st.session_state.job_count += 1
        if st.form_submit_button("✅ Done Submitting Income"):
            st.session_state.total_income = sum(x[1] for x in income_inputs)
            st.success(f"💼 Total Monthly Income: ${st.session_state.total_income:,.2f}")

    st.markdown("---")
    st.subheader("📦 Expenses")
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
        if st.form_submit_button("➕ Add Another Expense"):
            st.session_state.expense_count += 1
        if st.form_submit_button("✅ Done Submitting Expenses"):
            st.session_state.total_expense = sum(x[1] for x in expense_inputs)
            st.success(f"💸 Total Monthly Expenses: ${st.session_state.total_expense:,.2f}")

    if st.session_state.total_income and st.session_state.total_expense:
        net_balance = st.session_state.total_income - st.session_state.total_expense
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("💼 Total Income", f"${st.session_state.total_income:,.2f}", disabled=True)
        with col2:
            st.text_input("💸 Total Expenses", f"${st.session_state.total_expense:,.2f}", disabled=True)
        with col3:
            st.text_input("🧾 Remaining Balance After Expenses", f"${net_balance:,.2f}", disabled=True)

# ----------- TAB 2: Credit Cards ----------- #
with tabs[1]:
    st.subheader("💳 Credit Card Balances & Minimum Payments")
    card_inputs = []
    with st.form("card_form"):
        for i in range(st.session_state.card_count):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                name = st.text_input(f"Card {i+1} Name", value=f"Card {i+1}", key=f"card_name_{i}")
            with col2:
                balance = st.number_input(f"Balance", min_value=0.0, step=100.0, key=f"card_bal_{i}")
            with col3:
                min_pay = st.number_input(f"Min Payment", min_value=0.0, step=10.0, key=f"card_min_{i}")
            card_inputs.append((name, balance, min_pay))
        if st.form_submit_button("➕ Add Another Card"):
            st.session_state.card_count += 1
        if st.form_submit_button("✅ Done Submitting Cards"):
            st.session_state.total_min_pay = sum(x[2] for x in card_inputs)
            total_balance = sum(x[1] for x in card_inputs)
            st.success(f"📉 Total Card Balance: ${total_balance:,.2f}")
            st.success(f"💳 Total Minimum Payments: ${st.session_state.total_min_pay:,.2f}")

    if st.session_state.total_income and st.session_state.total_expense and st.session_state.total_min_pay:
        net_after_cards = st.session_state.total_income - st.session_state.total_expense - st.session_state.total_min_pay
        st.markdown("---")
        st.subheader("📊 Final Summary After Card Payments")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text_input("💼 Income", f"${st.session_state.total_income:,.2f}", disabled=True)
        with col2:
            st.text_input("💸 Expenses", f"${st.session_state.total_expense:,.2f}", disabled=True)
        with col3:
            st.text_input("💳 Min Payments", f"${st.session_state.total_min_pay:,.2f}", disabled=True)
        with col4:
            st.text_input("🧾 Remaining After Cards", f"${net_after_cards:,.2f}", disabled=True)

# ----------- TAB 3: Mortgage Readiness (DBS) ----------- #
with tabs[2]:
    st.subheader("📈 Mortgage Readiness – DBS Ratio Calculator")

    st.markdown("Enter your **gross monthly income** and **total monthly debt obligations** to estimate your DBS ratio.")

    monthly_income = st.number_input("Gross Monthly Income ($)", min_value=0.0, step=100.0, key="dbs_income")
    monthly_debts = st.number_input("Total Monthly Debt Payments ($)", min_value=0.0, step=50.0, key="dbs_debts")

    if st.button("📊 Calculate DBS Ratio"):
        if monthly_income > 0:
            dbs_ratio = (monthly_debts / monthly_income) * 100
            st.metric("Your DBS Ratio", f"{dbs_ratio:.2f}%")

            if dbs_ratio <= 36:
                st.success("✅ Excellent! You're well within the ideal mortgage approval range (≤ 36%).")
            elif dbs_ratio <= 44:
                st.warning("⚠️ Acceptable, but consider reducing your debt. Lenders may approve with caution.")
            else:
                st.error("🚫 High risk. Your DBS ratio is above recommended limits. Consider lowering debt or increasing income.")
        else:
            st.error("Please enter a valid income greater than $0.")
