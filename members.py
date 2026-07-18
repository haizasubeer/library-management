import streamlit as st
import pandas as pd
from db import fetch_all, fetch_one, execute_query

def get_all_members():
    rows = fetch_all("""
        SELECT Member_ID, Full_Name, Gender, Email, Phone,
               Membership_Type, Status
        FROM members ORDER BY Full_Name
    """)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def get_active_members():
    return fetch_all(
        "SELECT Member_ID, Full_Name FROM members WHERE Status='Active' ORDER BY Full_Name"
    )

def add_member(name, gender, email, phone, address, mem_type, status):
    if not name or not email or not phone:
        st.error("Name, Email and Phone are required.")
        return False
    if fetch_one("SELECT Member_ID FROM members WHERE Email=%s", (email,)):
        st.error(f"Email '{email}' already exists.")
        return False
    ok = execute_query("""
        INSERT INTO members (Full_Name,Gender,Email,Phone,Address,Membership_Type,Status)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (name, gender, email, phone, address, mem_type, status))
    if ok: st.success(f"Member '{name}' registered!")
    return ok

def render_members_page():
    st.header("👥 Members Management")
    tab1, tab2 = st.tabs(["View All Members", "Register New Member"])

    with tab1:
        df = get_all_members()
        if df.empty:
            st.info("No members found.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("add_member_form", clear_on_submit=True):
            name    = st.text_input("Full Name *")
            gender  = st.selectbox("Gender", ["Male","Female","Other"])
            email   = st.text_input("Email *")
            phone   = st.text_input("Phone * (10 digits)")
            address = st.text_area("Address")
            mtype   = st.selectbox("Membership Type", ["Standard","Premium","Student"])
            status  = st.selectbox("Status", ["Active","Inactive"])
            if st.form_submit_button("Register Member"):
                add_member(name, gender, email, phone, address, mtype, status)