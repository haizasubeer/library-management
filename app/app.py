import streamlit as st
from db import test_connection
from books import render_books_page
from members import render_members_page
from borrow import render_borrow_page
from reports import render_reports_page, get_kpis

# Setup clean page config
st.set_page_config(page_title="Library MS", page_icon="📚", layout="wide")

# Check database connection once on load
if "db_online" not in st.session_state:
    st.session_state.db_online = test_connection()

# ── Sidebar Navigation ────────────────────────────────────────
with st.sidebar:
    st.title("📚 LibraryMS")
    st.markdown("---")

    # Simple Connection Status Indicator
    if st.session_state.db_online:
        st.success("🟢 Connected to Database")
    else:
        st.error("🔴 Database Offline")
        
    st.markdown("---")
    
    page = st.radio("Navigation Menu", [
        "Home",
        "Books",
        "Members",
        "Borrow & Return",
        "Reports"
    ])

# ── Page Routing ──────────────────────────────────────────────
if page == "Home":
    st.title("Library Management System")
    st.write("Welcome to the library administration dashboard.")

    # Fetch live KPIs directly from the database
    kpis = get_kpis()
    
    # Fallback if DB is offline or empty
    if not kpis:
        kpis = {"total_books": 0, "available": 0, "members": 0, "borrowed": 0, "overdue": 0, "fines": 0}

    # Standard Streamlit Metric Columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Total Books", kpis.get("total_books", 0))
    col2.metric("Available", kpis.get("available", 0))
    col3.metric("Members", kpis.get("members", 0))
    col4.metric("On Loan", kpis.get("borrowed", 0))
    col5.metric("Overdue", kpis.get("overdue", 0))

    st.write("---")

    # Simple Alerts & Fines
    fines = kpis.get("fines", 0)
    st.metric("Total Library Fines Collected", f"₹{float(fines):,.2f}")
    
    overdue = kpis.get("overdue", 0)
    if overdue > 0:
        st.warning(f"Attention: There are currently {overdue} overdue books.")
    else:
        st.success("Excellent! All borrowed items are up to date.")

# Direct calls to your actual database frontend modules
elif page == "Books":
    render_books_page()

elif page == "Members":
    render_members_page()

elif page == "Borrow & Return":
    render_borrow_page()

elif page == "Reports":
    render_reports_page()