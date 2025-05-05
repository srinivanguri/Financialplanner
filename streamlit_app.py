import streamlit as st
import sqlite3

# DB setup
conn = sqlite3.connect("tacsis.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS incomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    amount REAL,
    frequency TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount REAL,
    recurring BOOLEAN
)
""")
conn.commit()

# Helper functions
def add_income(source, amount, frequency):
    cursor.execute("INSERT INTO incomes (source, amount, frequency) VALUES (?, ?, ?)", (source, amount, frequency))
    conn.commit()

def add_expense(category, amount, recurring):
    cursor.execute("INSERT INTO expenses (category, amount, recurring) VALUES (?, ?, ?)", (category, amount, recurring))
    conn.commit()

def get_total_income():
    cursor.execute("SELECT amount, frequency FROM incomes")
    rows = cursor.fetchall()
    total = 0
    for amount, freq in rows:
        if freq == "monthly":
            total += amount
        elif freq == "biweekly":
            total += (amount * 26) / 12
    return round(total, 2)

def get_total_expenses():
    cursor.execute("SELECT amount FROM expenses WHERE recurring = 1")
    rows = cursor.fetchall()
    return round(sum(row[0] for row in rows), 2)

def get_net_savings():
    return get_total_income() - get_total_expenses()

# UI
st.set_page_config(page_title="TACSiS Budget Planner", layout="centered")
st.title("💰 TACSiS – Budget Planner MVP")

tab1, tab2, tab3 = st.tabs(["➕ Add", "📊 Summary", "📁 Records"])

with tab1:
    st.header("Add Income")
st.info("💡 You can add multiple income sources separately — like Job 1, Freelance, Side Hustle, etc.")

source = st.text_input("Income Source (e.g., Job 1, Freelance)")
amount = st.number_input("Amount", min_value=0.0, key="income_amt")
frequency = st.selectbox("Frequency", ["monthly", "biweekly"])

if st.button("Add Income"):
    if source and amount > 0:
        add_income(source, amount, frequency)
        st.success(f"✅ Income '{source}' added!")
    else:
        st.warning("⚠️ Please enter a source and amount.")

    st.header("Add Expense")
    category = st.text_input("Expense Category")
    exp_amount = st.number_input("Expense Amount", min_value=0.0, key="exp")
    recurring = st.checkbox("Recurring", value=True)
    if st.button("Add Expense"):
        add_expense(category, exp_amount, recurring)
        st.success("Expense added!")

with tab2:
    st.header("📊 Monthly Summary")
    st.metric("Total Income", f"${get_total_income():,.2f}")
    st.metric("Total Expenses", f"${get_total_expenses():,.2f}")
    st.metric("Net Savings", f"${get_net_savings():,.2f}")

with tab3:
    st.header("All Incomes")
    cursor.execute("SELECT source, amount, frequency FROM incomes")
    st.dataframe(cursor.fetchall(), use_container_width=True)

    st.header("All Expenses")
    cursor.execute("SELECT category, amount, recurring FROM expenses")
    st.dataframe(cursor.fetchall(), use_container_width=True)

st.sidebar.markdown("### 📬 Feedback")
st.sidebar.markdown("We value your input — help us improve!")
st.sidebar.markdown("[👉 Take our quick survey](https://forms.gle/VScw26geNBzwXoFX7)")

