import streamlit as st
import pandas as pd
from db import fetch_all, fetch_one, execute_query

def get_all_books():
    rows = fetch_all("""
        SELECT b.Book_ID, b.ISBN, b.Title, b.Author,
               c.Category_Name AS Category,
               b.Total_Copies, b.Available_Copies, b.Shelf_Number
        FROM books b
        JOIN categories c ON b.Category_ID = c.Category_ID
        ORDER BY b.Title
    """)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def get_categories():
    return fetch_all("SELECT Category_ID, Category_Name FROM categories ORDER BY Category_Name")

def add_book(isbn, title, author, category_id, publisher, year, total, available, shelf):
    if not title or not author or not isbn:
        st.error("Title, Author and ISBN are required.")
        return False
    if fetch_one("SELECT Book_ID FROM books WHERE ISBN=%s", (isbn,)):
        st.error(f"ISBN '{isbn}' already exists.")
        return False
    ok = execute_query("""
        INSERT INTO books (ISBN,Title,Author,Category_ID,Publisher,
                           Publication_Year,Total_Copies,Available_Copies,Shelf_Number)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (isbn, title, author, category_id, publisher, year, total, available, shelf))
    if ok: st.success(f"Book '{title}' added!")
    return ok

def render_books_page():
    st.header("📚 Books Management")
    cats = get_categories()
    cat_map = {c["Category_Name"]: c["Category_ID"] for c in cats}

    tab1, tab2 = st.tabs(["View All Books", "Add New Book"])

    with tab1:
        df = get_all_books()
        if df.empty:
            st.info("No books found.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("add_book_form", clear_on_submit=True):
            isbn   = st.text_input("ISBN *")
            title  = st.text_input("Title *")
            author = st.text_input("Author *")
            cat    = st.selectbox("Category", list(cat_map.keys()))
            pub    = st.text_input("Publisher")
            year   = st.number_input("Year", 1800, 2100, 2024)
            total  = st.number_input("Total Copies", 1, 100, 1)
            avail  = st.number_input("Available Copies", 0, 100, 1)
            shelf  = st.text_input("Shelf Number")
            if st.form_submit_button("Add Book"):
                add_book(isbn, title, author, cat_map[cat], pub, year, total, avail, shelf)