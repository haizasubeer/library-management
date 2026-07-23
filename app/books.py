import streamlit as st
import pandas as pd
from db import get_books_df, save_books_df

CATEGORIES = [
    "Computer Science", "Mathematics", "Physics", "Literature",
    "History", "Business & Finance", "Science Fiction", 
    "Self Help", "Biology", "Engineering", "General Knowledge"
]

def add_book(isbn, title, author, category, publisher, year, total, shelf):
    if not title or not author or not isbn:
        st.error("❌ Title, Author, and ISBN are required.")
        return False
    
    df = get_books_df()
    
    # Check ISBN unique
    if not df.empty and isbn in df["ISBN"].astype(str).values:
        st.error(f"❌ Book with ISBN '{isbn}' already exists in inventory.")
        return False

    new_id = int(df["Book_ID"].max() + 1) if not df.empty and len(df) > 0 else 1

    new_row = {
        "Book_ID": new_id,
        "ISBN": str(isbn),
        "Title": str(title),
        "Author": str(author),
        "Category": str(category),
        "Publisher": str(publisher),
        "Publication_Year": int(year),
        "Total_Copies": int(total),
        "Available_Copies": int(total),
        "Shelf_Number": str(shelf)
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_books_df(df)
    st.success(f"🎉 Book '{title}' added successfully to CSV database!")
    return True

def render_books_page():
    st.markdown("<h2 style='color:#ff007f;'>📚 Books Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View Inventory", "➕ Add New Book"])

    with tab1:
        df = get_books_df()
        if df.empty:
            st.info("No books found in the database. Add your first book below!")
        else:
            # Search box
            search_query = st.text_input("🔍 Search books by Title, Author, or Category", "")
            if search_query:
                filtered_df = df[
                    df["Title"].str.contains(search_query, case=False, na=False) |
                    df["Author"].str.contains(search_query, case=False, na=False) |
                    df["Category"].str.contains(search_query, case=False, na=False)
                ]
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("add_book_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                isbn = st.text_input("ISBN Code *", placeholder="e.g. 978-0134685991")
                title = st.text_input("Book Title *")
                author = st.text_input("Author Name *")
                category = st.selectbox("Category", CATEGORIES)
            with col_b:
                publisher = st.text_input("Publisher", placeholder="e.g. Pearson")
                year = st.number_input("Publication Year", 1800, 2100, 2024)
                total = st.number_input("Total Copies", 1, 100, 5)
                shelf = st.text_input("Shelf Location", placeholder="e.g. CS-A1")

            if st.form_submit_button("➕ Save Book to Database"):
                if add_book(isbn, title, author, category, publisher, year, total, shelf):
                    st.rerun()