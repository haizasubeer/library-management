"""
==============================================================
 Library Management System
 File        : db.py
 Description : CSV Database Access Layer using Pandas.
               Replaces MySQL to allow 100% zero-config deployment
               on Streamlit Cloud.
==============================================================
"""

import os
import pandas as pd
from datetime import date

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_CSV = os.path.join(BASE_DIR, "books.csv")
MEMBERS_CSV = os.path.join(BASE_DIR, "members.csv")
BORROW_CSV = os.path.join(BASE_DIR, "borrow_records.csv")

def init_csv_files():
    """Ensures CSV files exist with proper headers if missing."""
    if not os.path.exists(BOOKS_CSV):
        df_books = pd.DataFrame(columns=[
            "Book_ID", "ISBN", "Title", "Author", "Category", 
            "Publisher", "Publication_Year", "Total_Copies", "Available_Copies", "Shelf_Number"
        ])
        df_books.to_csv(BOOKS_CSV, index=False)

    if not os.path.exists(MEMBERS_CSV):
        df_members = pd.DataFrame(columns=[
            "Member_ID", "Full_Name", "Gender", "Email", 
            "Phone", "Address", "Membership_Type", "Status"
        ])
        df_members.to_csv(MEMBERS_CSV, index=False)

    if not os.path.exists(BORROW_CSV):
        df_borrow = pd.DataFrame(columns=[
            "Borrow_ID", "Member_ID", "Book_ID", 
            "Borrow_Date", "Due_Date", "Return_Date", "Fine_Amount", "Borrow_Status"
        ])
        df_borrow.to_csv(BORROW_CSV, index=False)

# ── Data Loaders & Savers ──────────────────────────────────────
def get_books_df():
    init_csv_files()
    df = pd.read_csv(BOOKS_CSV, dtype={"ISBN": str, "Phone": str, "Shelf_Number": str})
    return df

def save_books_df(df):
    df.to_csv(BOOKS_CSV, index=False)

def get_members_df():
    init_csv_files()
    df = pd.read_csv(MEMBERS_CSV, dtype={"Phone": str})
    return df

def save_members_df(df):
    df.to_csv(MEMBERS_CSV, index=False)

def get_borrow_df():
    init_csv_files()
    df = pd.read_csv(BORROW_CSV)
    return df

def save_borrow_df(df):
    df.to_csv(BORROW_CSV, index=False)

def test_connection():
    """Always returns True because CSV storage is local and serverless."""
    init_csv_files()
    return True

# ── KPI Helper ─────────────────────────────────────────────────
def get_kpis():
    init_csv_files()
    books_df = get_books_df()
    members_df = get_members_df()
    borrow_df = get_borrow_df()

    today_str = str(date.today())

    # Update overdue status dynamically
    if not borrow_df.empty:
        overdue_mask = (
            (borrow_df["Borrow_Status"] == "Borrowed") & 
            (borrow_df["Due_Date"] < today_str)
        )
        borrow_df.loc[overdue_mask, "Borrow_Status"] = "Overdue"
        
        # Calculate dynamic fine: ₹5 per day overdue
        for idx in borrow_df[borrow_df["Borrow_Status"] == "Overdue"].index:
            due_dt = date.fromisoformat(str(borrow_df.loc[idx, "Due_Date"]))
            days_late = (date.today() - due_dt).days
            borrow_df.loc[idx, "Fine_Amount"] = max(0.0, float(days_late * 5.0))
            
        save_borrow_df(borrow_df)

    total_books = int(books_df["Total_Copies"].sum()) if not books_df.empty else 0
    available = int(books_df["Available_Copies"].sum()) if not books_df.empty else 0
    active_members = len(members_df[members_df["Status"] == "Active"]) if not members_df.empty else 0
    borrowed = len(borrow_df[borrow_df["Borrow_Status"].isin(["Borrowed", "Overdue"])]) if not borrow_df.empty else 0
    overdue = len(borrow_df[borrow_df["Borrow_Status"] == "Overdue"]) if not borrow_df.empty else 0
    fines = float(borrow_df["Fine_Amount"].sum()) if not borrow_df.empty else 0.0

    return {
        "total_books": total_books,
        "available": available,
        "members": active_members,
        "borrowed": borrowed,
        "overdue": overdue,
        "fines": fines
    }