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
    st.caption("Manage your books, tracking, and memberships seamlessly.")
    st.write("---")
    kpis = get_kpis()
    total_books = kpis.get("total_books", 0)
    available   = kpis.get("available", 0)
    members     = kpis.get("members", 0)
    borrowed    = kpis.get("borrowed", 0)
    overdue     = kpis.get("overdue", 0)

    c1,c2,c3,c4,c5 = st.columns(5)

    with c1:
        with st.container(border=True):
            st.metric(label="📘 Total Books", value=f"{total_books:,}")
            
    with c2:
        with st.container(border=True):
            st.metric(label="🟢 Available", value=f"{available:,}")
    with c3:
        with st.container(border=True):
            st.metric(label="👥 Active Members", value=f"{members:,}")
            
    with c4:
        with st.container(border=True):
            st.metric(label="📙 On Loan", value=f"{borrowed:,}")
            
    with c5:
        with st.container(border=True):
            st.metric(label="⚠️ Overdue Items", value=overdue)

    st.write("---")
    if overdue > 0:
        st.error(f"🚨 Action Required: There are currently {overdue} overdue books that need attention.")
    else:
        st.success("✨ Excellent! All borrowed books are currently on track and within schedule.")
        
elif page == "📚 Books":
    render_books_page()

elif page == "👥 Members":
    render_members_page()

elif page == "📖 Borrow & Return":
    render_borrow_page()

elif page == "📊 Reports":
    render_reports_page()