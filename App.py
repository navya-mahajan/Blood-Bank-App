import streamlit as st
from database import *
from datetime import timedelta, datetime

create_tables()

st.set_page_config(page_title="Blood Bank App", layout="wide")

st.title("Blood Bank Management System")
st.markdown("### Manage donors, blood units and inventory easily")

menu = ["Home", "Donor Registration", "Blood Collection", "Inventory", "Issue Blood"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- HOME ----------------
if choice == "Home":
    st.subheader("Welcome")
    st.write("This app helps manage blood bank operations efficiently.")
    st.write("Last Updated:", datetime.now())

# ---------------- DONOR ----------------
elif choice == "Donor Registration":
    st.subheader("Donor Registration")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=65)
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    phone = st.text_input("Phone")

    if st.button("Register"):
        add_donor(name, age, blood_group, phone)
        st.success("Donor Registered Successfully")
        st.rerun()

# ---------------- COLLECTION ----------------
elif choice == "Blood Collection":
    st.subheader("Blood Collection")

    bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    collection_date = st.date_input("Collection Date")

    expiry_date = collection_date + timedelta(days=30)
    st.write(f"Expiry Date: {expiry_date}")

    if st.button("Add Blood"):
        add_blood(bg, str(collection_date), str(expiry_date))
        st.success("Blood Unit Added")
        st.rerun()

# ---------------- INVENTORY ----------------
elif choice == "Inventory":
    st.subheader("Inventory Dashboard")

    st.caption("Data updates in real-time as changes are made")

    data = get_inventory()

    if data:
        import pandas as pd
        df = pd.DataFrame(data, columns=["Blood Group", "Units"])

        st.dataframe(df)

        total = df["Units"].sum()
        st.metric("Total Available Units", total)

        # Low stock alert
        low_stock = df[df["Units"] < 2]
        if not low_stock.empty:
            st.error("Low Stock Alert!")
            st.dataframe(low_stock)

    else:
        st.warning("No Data Available")

# ---------------- ISSUE ----------------
elif choice == "Issue Blood":
    st.subheader("Issue Blood")

    bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

    if st.button("Issue"):
        if issue_blood(bg):
            st.success("Blood Issued Successfully")
        else:
            st.error("Blood Not Available")
        st.rerun()
