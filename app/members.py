"""
==============================================================
 Library Management System
 File        : members.py
 Description : Members Directory module powered by CSV Database.
==============================================================
"""

import streamlit as st
import pandas as pd
from db import get_members_df, save_members_df

def add_member(name, gender, email, phone, address, mem_type, status):
    if not name or not email or not phone:
        st.error("❌ Name, Email, and Phone number are required.")
        return False
    
    df = get_members_df()
    
    # Check Email unique
    if not df.empty and email in df["Email"].astype(str).values:
        st.error(f"❌ Member with Email '{email}' is already registered.")
        return False

    new_id = int(df["Member_ID"].max() + 1) if not df.empty and len(df) > 0 else 1

    new_row = {
        "Member_ID": new_id,
        "Full_Name": str(name),
        "Gender": str(gender),
        "Email": str(email),
        "Phone": str(phone),
        "Address": str(address),
        "Membership_Type": str(mem_type),
        "Status": str(status)
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_members_df(df)
    st.success(f"🎉 Member '{name}' registered successfully!")
    return True

def render_members_page():
    st.markdown("<h2 style='color:#00f0ff;'>👥 Members Directory</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View Directory", "➕ Register New Member"])

    with tab1:
        df = get_members_df()
        if df.empty:
            st.info("No members registered yet.")
        else:
            search_query = st.text_input("🔍 Search member by Name, Email, or Phone", "")
            if search_query:
                filtered_df = df[
                    df["Full_Name"].str.contains(search_query, case=False, na=False) |
                    df["Email"].str.contains(search_query, case=False, na=False) |
                    df["Phone"].astype(str).str.contains(search_query, case=False, na=False)
                ]
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("add_member_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Full Name *")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                email = st.text_input("Email Address *")
            with col_b:
                phone = st.text_input("Phone Number *")
                mem_type = st.selectbox("Membership Tier", ["Standard", "Premium", "Student"])
                status = st.selectbox("Status", ["Active", "Inactive", "Suspended"])
            
            address = st.text_area("Home Address", placeholder="Enter address details...")

            if st.form_submit_button("➕ Register Member"):
                if add_member(name, gender, email, phone, address, mem_type, status):
                    st.rerun()