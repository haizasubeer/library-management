import streamlit as st
import pandas as pd
import plotly.express as px
from db import fetch_all, fetch_one

def get_kpis():
    return fetch_one("""
        SELECT
            (SELECT COUNT(*) FROM books)                           AS total_books,
            (SELECT SUM(Available_Copies) FROM books)              AS available,
            (SELECT COUNT(*) FROM members WHERE Status='Active')   AS members,
            (SELECT COUNT(*) FROM borrow_records
             WHERE Borrow_Status IN ('Borrowed','Overdue'))        AS borrowed,
            (SELECT COUNT(*) FROM borrow_records
             WHERE Borrow_Status='Overdue')                        AS overdue,
            (SELECT COALESCE(SUM(Fine_Amount),0)
             FROM borrow_records WHERE Borrow_Status='Returned')   AS fines
    """) or {}

def render_reports_page():
    st.header("📊 Reports & Analytics")
    kpis = get_kpis()

    col1,col2,col3,col4,col5 = st.columns(5)
    col1.metric("Total Books",   kpis.get("total_books",0))
    col2.metric("Available",     kpis.get("available",0))
    col3.metric("Members",       kpis.get("members",0))
    col4.metric("Borrowed",      kpis.get("borrowed",0))
    col5.metric("Overdue",       kpis.get("overdue",0))

    st.markdown("---")

    # Most borrowed books
    rows = fetch_all("""
        SELECT b.Title, COUNT(*) AS Borrows
        FROM borrow_records br
        JOIN books b ON br.Book_ID=b.Book_ID
        GROUP BY b.Book_ID, b.Title
        ORDER BY Borrows DESC LIMIT 10
    """)
    if rows:
        df = pd.DataFrame(rows)
        fig = px.bar(df, x="Borrows", y="Title", orientation="h",
                     title="Top 10 Most Borrowed Books",
                     color="Borrows", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

    # Books by category
    rows2 = fetch_all("""
        SELECT c.Category_Name AS Category, COUNT(b.Book_ID) AS Books
        FROM categories c LEFT JOIN books b ON c.Category_ID=b.Category_ID
        GROUP BY c.Category_ID, c.Category_Name
    """)
    if rows2:
        df2 = pd.DataFrame(rows2)
        fig2 = px.pie(df2, names="Category", values="Books",
                      title="Books by Category", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader(f"Total Fines Collected: ₹{float(kpis.get('fines',0)):,.2f}")