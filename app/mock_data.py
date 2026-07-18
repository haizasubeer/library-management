"""
==============================================================
 Library Management System
 File        : mock_data.py
 Description : Emulates MySQL database tables and CRUD operations
               in Python memory using Streamlit Session State.
               Used for a colorful interactive demo when MySQL
               is not connected.
==============================================================
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Initialize Mock Session State Data
def init_mock_data():
    if "mock_initialized" not in st.session_state:
        st.session_state.mock_initialized = True
        
        # Categories
        st.session_state.mock_categories = [
            {"Category_ID": 1, "Category_Name": "Computer Science"},
            {"Category_ID": 2, "Category_Name": "Mathematics"},
            {"Category_ID": 3, "Category_Name": "Physics"},
            {"Category_ID": 4, "Category_Name": "Literature"},
            {"Category_ID": 5, "Category_Name": "History"},
            {"Category_ID": 6, "Category_Name": "Business & Finance"},
            {"Category_ID": 7, "Category_Name": "Science Fiction"},
            {"Category_ID": 8, "Category_Name": "Self Help"},
            {"Category_ID": 9, "Category_Name": "Biology"},
            {"Category_ID": 10, "Category_Name": "Engineering"}
        ]
        
        # Books
        st.session_state.mock_books = [
            {"Book_ID": 1, "ISBN": "978-0134685991", "Title": "Effective Java", "Author": "Joshua Bloch", "Category_ID": 1, "Publisher": "Addison-Wesley", "Publication_Year": 2018, "Total_Copies": 10, "Available_Copies": 8, "Shelf_Number": "CS-A1"},
            {"Book_ID": 2, "ISBN": "978-0132350884", "Title": "Clean Code", "Author": "Robert C. Martin", "Category_ID": 1, "Publisher": "Prentice Hall", "Publication_Year": 2008, "Total_Copies": 8, "Available_Copies": 6, "Shelf_Number": "CS-A2"},
            {"Book_ID": 3, "ISBN": "978-0131401921", "Title": "Calculus", "Author": "James Stewart", "Category_ID": 2, "Publisher": "Cengage", "Publication_Year": 2015, "Total_Copies": 5, "Available_Copies": 4, "Shelf_Number": "MA-A1"},
            {"Book_ID": 4, "ISBN": "978-0393093025", "Title": "A Brief History of Time", "Author": "Stephen Hawking", "Category_ID": 3, "Publisher": "Bantam Books", "Publication_Year": 1998, "Total_Copies": 7, "Available_Copies": 7, "Shelf_Number": "PH-A1"},
            {"Book_ID": 5, "ISBN": "978-0743273565", "Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald", "Category_ID": 4, "Publisher": "Scribner", "Publication_Year": 2004, "Total_Copies": 12, "Available_Copies": 10, "Shelf_Number": "LI-A1"},
            {"Book_ID": 6, "ISBN": "978-0393347975", "Title": "Sapiens", "Author": "Yuval Noah Harari", "Category_ID": 5, "Publisher": "Harper", "Publication_Year": 2015, "Total_Copies": 15, "Available_Copies": 13, "Shelf_Number": "HI-A1"},
            {"Book_ID": 7, "ISBN": "978-0066620992", "Title": "Good to Great", "Author": "Jim Collins", "Category_ID": 6, "Publisher": "HarperBusiness", "Publication_Year": 2001, "Total_Copies": 6, "Available_Copies": 5, "Shelf_Number": "BU-A1"},
            {"Book_ID": 8, "ISBN": "978-0441013593", "Title": "Dune", "Author": "Frank Herbert", "Category_ID": 7, "Publisher": "Ace Books", "Publication_Year": 1990, "Total_Copies": 9, "Available_Copies": 8, "Shelf_Number": "SF-A1"},
            {"Book_ID": 9, "ISBN": "978-1501143519", "Title": "Atomic Habits", "Author": "James Clear", "Category_ID": 8, "Publisher": "Avery", "Publication_Year": 2018, "Total_Copies": 20, "Available_Copies": 18, "Shelf_Number": "SH-A1"},
            {"Book_ID": 10, "ISBN": "978-0393350685", "Title": "The Selfish Gene", "Author": "Richard Dawkins", "Category_ID": 9, "Publisher": "Oxford UP", "Publication_Year": 2016, "Total_Copies": 4, "Available_Copies": 4, "Shelf_Number": "BI-A1"}
        ]
        
        # Members
        st.session_state.mock_members = [
            {"Member_ID": 1, "Full_Name": "Aarav Sharma", "Gender": "Male", "Email": "aarav@email.com", "Phone": "9876543210", "Address": "New Delhi", "Membership_Type": "Standard", "Status": "Active"},
            {"Member_ID": 2, "Full_Name": "Priya Patel", "Gender": "Female", "Email": "priya@email.com", "Phone": "9123456780", "Address": "Mumbai", "Membership_Type": "Premium", "Status": "Active"},
            {"Member_ID": 3, "Full_Name": "Rohit Kumar", "Gender": "Male", "Email": "rohit@email.com", "Phone": "9988776655", "Address": "Bangalore", "Membership_Type": "Student", "Status": "Active"},
            {"Member_ID": 4, "Full_Name": "Ananya Singh", "Gender": "Female", "Email": "ananya@email.com", "Phone": "9845123456", "Address": "Lucknow", "Membership_Type": "Standard", "Status": "Active"},
            {"Member_ID": 5, "Full_Name": "Vikram Mehta", "Gender": "Male", "Email": "vikram@email.com", "Phone": "9911223344", "Address": "Chandigarh", "Membership_Type": "Premium", "Status": "Active"}
        ]
        
        # Borrow Records
        today = date.today()
        st.session_state.mock_borrows = [
            {"Borrow_ID": 1, "Member_ID": 1, "Book_ID": 1, "Borrow_Date": today - timedelta(days=10), "Due_Date": today + timedelta(days=4), "Return_Date": None, "Fine_Amount": 0.0, "Borrow_Status": "Borrowed"},
            {"Borrow_ID": 2, "Member_ID": 2, "Book_ID": 2, "Borrow_Date": today - timedelta(days=20), "Due_Date": today - timedelta(days=6), "Return_Date": None, "Fine_Amount": 30.0, "Borrow_Status": "Overdue"},
            {"Borrow_ID": 3, "Member_ID": 3, "Book_ID": 5, "Borrow_Date": today - timedelta(days=15), "Due_Date": today - timedelta(days=1), "Return_Date": today, "Fine_Amount": 5.0, "Borrow_Status": "Returned"},
            {"Borrow_ID": 4, "Member_ID": 4, "Book_ID": 9, "Borrow_Date": today - timedelta(days=5), "Due_Date": today + timedelta(days=9), "Return_Date": None, "Fine_Amount": 0.0, "Borrow_Status": "Borrowed"}
        ]

# Helper to map categories
def get_cat_name(cat_id):
    for c in st.session_state.mock_categories:
        if c["Category_ID"] == cat_id:
            return c["Category_Name"]
    return "Unknown"

# Emulate Books CRUD
def mock_get_all_books():
    init_mock_data()
    books = []
    for b in st.session_state.mock_books:
        bk = b.copy()
        bk["Category"] = get_cat_name(b["Category_ID"])
        books.append(bk)
    df = pd.DataFrame(books)
    if not df.empty:
        df = df[["Book_ID", "ISBN", "Title", "Author", "Category", "Total_Copies", "Available_Copies", "Shelf_Number"]]
    return df

def mock_add_book(isbn, title, author, category_id, publisher, year, total, available, shelf):
    init_mock_data()
    # Check ISBN unique
    for b in st.session_state.mock_books:
        if b["ISBN"] == isbn:
            st.error(f"ISBN '{isbn}' already exists.")
            return False
            
    new_id = max([b["Book_ID"] for b in st.session_state.mock_books]) + 1
    st.session_state.mock_books.append({
        "Book_ID": new_id, "ISBN": isbn, "Title": title, "Author": author,
        "Category_ID": category_id, "Publisher": publisher, "Publication_Year": year,
        "Total_Copies": total, "Available_Copies": available, "Shelf_Number": shelf
    })
    st.success(f"Book '{title}' added to Demo Mode!")
    return True

# Emulate Members CRUD
def mock_get_all_members():
    init_mock_data()
    return pd.DataFrame(st.session_state.mock_members)

def mock_get_active_members():
    init_mock_data()
    return [m for m in st.session_state.mock_members if m["Status"] == "Active"]

def mock_add_member(name, gender, email, phone, address, mem_type, status):
    init_mock_data()
    for m in st.session_state.mock_members:
        if m["Email"] == email:
            st.error(f"Email '{email}' already exists.")
            return False
    new_id = max([m["Member_ID"] for m in st.session_state.mock_members]) + 1
    st.session_state.mock_members.append({
        "Member_ID": new_id, "Full_Name": name, "Gender": gender,
        "Email": email, "Phone": phone, "Address": address,
        "Membership_Type": mem_type, "Status": status
    })
    st.success(f"Member '{name}' registered in Demo Mode!")
    return True

# Emulate Borrow
def mock_get_active_borrows():
    init_mock_data()
    borrows = []
    for br in st.session_state.mock_borrows:
        if br["Borrow_Status"] in ["Borrowed", "Overdue"]:
            member_name = "Unknown"
            book_title = "Unknown"
            for m in st.session_state.mock_members:
                if m["Member_ID"] == br["Member_ID"]:
                    member_name = m["Full_Name"]
            for b in st.session_state.mock_books:
                if b["Book_ID"] == br["Book_ID"]:
                    book_title = b["Title"]
            borrows.append({
                "Borrow_ID": br["Borrow_ID"],
                "Member": member_name,
                "Book": book_title,
                "Borrow_Date": br["Borrow_Date"],
                "Due_Date": br["Due_Date"],
                "Borrow_Status": br["Borrow_Status"]
            })
    return pd.DataFrame(borrows)

def mock_borrow_book(member_id, book_id, due_date):
    init_mock_data()
    # Check book copies
    for b in st.session_state.mock_books:
        if b["Book_ID"] == book_id:
            if b["Available_Copies"] < 1:
                st.error("No copies available.")
                return False
            b["Available_Copies"] -= 1
            book_title = b["Title"]
            
    member_name = "Member"
    for m in st.session_state.mock_members:
        if m["Member_ID"] == member_id:
            member_name = m["Full_Name"]
            
    new_id = max([br["Borrow_ID"] for br in st.session_state.mock_borrows]) + 1
    st.session_state.mock_borrows.append({
        "Borrow_ID": new_id, "Member_ID": member_id, "Book_ID": book_id,
        "Borrow_Date": date.today(), "Due_Date": due_date, "Return_Date": None,
        "Fine_Amount": 0.0, "Borrow_Status": "Borrowed"
    })
    st.success(f"'{book_title}' issued to {member_name} (Demo Mode)!")
    return True

def mock_return_book(borrow_id):
    init_mock_data()
    for br in st.session_state.mock_borrows:
        if br["Borrow_ID"] == borrow_id:
            if br["Borrow_Status"] == "Returned":
                st.error("Already returned.")
                return False
            
            # Update book copies
            for b in st.session_state.mock_books:
                if b["Book_ID"] == br["Book_ID"]:
                    b["Available_Copies"] += 1
            
            today = date.today()
            due = br["Due_Date"]
            fine = max(0, (today - due).days) * 5.00 if today > due else 0.0
            
            br["Return_Date"] = today
            br["Fine_Amount"] = fine
            br["Borrow_Status"] = "Returned"
            
            if fine > 0:
                st.warning(f"Returned! Fine: ₹{fine:.2f} (Demo Mode)")
            else:
                st.success("Returned on time. No fine. (Demo Mode)")
            return True
            
    st.error("Borrow ID not found in Demo Mode.")
    return False

# Emulate Reports
def mock_get_kpis():
    init_mock_data()
    total_books = sum([b["Total_Copies"] for b in st.session_state.mock_books])
    available = sum([b["Available_Copies"] for b in st.session_state.mock_books])
    members = len([m for m in st.session_state.mock_members if m["Status"] == "Active"])
    borrowed = len([br for br in st.session_state.mock_borrows if br["Borrow_Status"] in ["Borrowed", "Overdue"]])
    overdue = len([br for br in st.session_state.mock_borrows if br["Borrow_Status"] == "Overdue"])
    fines = sum([br["Fine_Amount"] for br in st.session_state.mock_borrows])
    return {
        "total_books": len(st.session_state.mock_books),
        "available": available,
        "members": members,
        "borrowed": borrowed,
        "overdue": overdue,
        "fines": fines
    }

def mock_get_most_borrowed_books():
    init_mock_data()
    # Simple count simulation
    counts = {1: 15, 2: 12, 5: 25, 9: 18}
    rows = []
    for b in st.session_state.mock_books:
        bid = b["Book_ID"]
        if bid in counts:
            rows.append({"Title": b["Title"], "Borrows": counts[bid]})
    # sort
    rows = sorted(rows, key=lambda x: x["Borrows"], reverse=True)
    return rows

def mock_get_books_by_category():
    init_mock_data()
    cat_counts = {}
    for b in st.session_state.mock_books:
        cname = get_cat_name(b["Category_ID"])
        cat_counts[cname] = cat_counts.get(cname, 0) + 1
    
    rows = [{"Category": c, "Books": count} for c, count in cat_counts.items()]
    return rows
