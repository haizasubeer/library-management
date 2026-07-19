import streamlit as st
from db      import test_connection
from books   import render_books_page
from members import render_members_page
from borrow  import render_borrow_page
from reports import render_reports_page, get_kpis

st.set_page_config(page_title="Library MS", page_icon="📚", layout="wide")

with st.sidebar:
    st.markdown("## 📚 LibraryMS")
    if test_connection():
        st.success("🟢 DB Connected")
    else:
        st.error("🔴 DB Offline")
    page = st.radio("Navigation", [
        "🏠 Home",
        "📚 Books",
        "👥 Members",
        "📖 Borrow & Return",
        "📊 Reports"
    ])

if page == "🏠 Home":
    st.title("📚 Library Management System")
    st.markdown("Use the **sidebar** to navigate.")
    kpis = get_kpis()
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Books",    kpis.get("total_books",0))
    c2.metric("Available",kpis.get("available",0))
    c3.metric("Members",  kpis.get("members",0))
    c4.metric("Borrowed", kpis.get("borrowed",0))
    c5.metric("Overdue",  kpis.get("overdue",0))

elif page == "📚 Books":
    render_books_page()

elif page == "👥 Members":
    render_members_page()

elif page == "📖 Borrow & Return":
    render_borrow_page()

elif page == "📊 Reports":
    render_reports_page()