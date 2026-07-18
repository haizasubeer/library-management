import streamlit as st
import pandas as pd
from datetime import date, timedelta
from db import fetch_all, fetch_one, execute_query

FINE_PER_DAY = 5.00

def get_active_borrows():
    rows = fetch_all("""
        SELECT br.Borrow_ID, m.Full_Name AS Member, b.Title AS Book,
               br.Borrow_Date, br.Due_Date, br.Borrow_Status
        FROM borrow_records br
        JOIN members m ON br.Member_ID = m.Member_ID
        JOIN books   b ON br.Book_ID   = b.Book_ID
        WHERE br.Borrow_Status IN ('Borrowed','Overdue')
        ORDER BY br.Due_Date
    """)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def borrow_book(member_id, book_id, due_date):
    member = fetch_one("SELECT Full_Name, Status FROM members WHERE Member_ID=%s", (member_id,))
    if not member or member["Status"] != "Active":
        st.error("Member not found or not Active.")
        return False
    book = fetch_one("SELECT Title, Available_Copies FROM books WHERE Book_ID=%s", (book_id,))
    if not book or book["Available_Copies"] < 1:
        st.error("Book not available.")
        return False
    ok = execute_query("""
        INSERT INTO borrow_records (Member_ID,Book_ID,Borrow_Date,Due_Date,Borrow_Status)
        VALUES (%s,%s,%s,%s,'Borrowed')
    """, (member_id, book_id, date.today(), due_date))
    if ok:
        execute_query("UPDATE books SET Available_Copies=Available_Copies-1 WHERE Book_ID=%s", (book_id,))
        st.success(f"'{book['Title']}' issued to {member['Full_Name']}!")
    return ok

def return_book(borrow_id):
    rec = fetch_one("""
        SELECT br.*, b.Title, m.Full_Name
        FROM borrow_records br
        JOIN books b ON br.Book_ID=b.Book_ID
        JOIN members m ON br.Member_ID=m.Member_ID
        WHERE br.Borrow_ID=%s
    """, (borrow_id,))
    if not rec:
        st.error("Borrow record not found.")
        return False
    if rec["Borrow_Status"] == "Returned":
        st.error("Already returned.")
        return False
    today = date.today()
    due   = rec["Due_Date"]
    fine  = max(0, (today - due).days) * FINE_PER_DAY if today > due else 0.0
    ok = execute_query("""
        UPDATE borrow_records
        SET Return_Date=%s, Fine_Amount=%s, Borrow_Status='Returned'
        WHERE Borrow_ID=%s
    """, (today, fine, borrow_id))
    if ok:
        execute_query("UPDATE books SET Available_Copies=Available_Copies+1 WHERE Book_ID=%s",
                      (rec["Book_ID"],))
        if fine > 0:
            st.warning(f"Returned! Fine: ₹{fine:.2f}")
        else:
            st.success("Returned on time. No fine.")
    return ok

def render_borrow_page():
    st.header("📖 Borrow & Return")
    from members import get_active_members

    tab1, tab2, tab3 = st.tabs(["Issue Book","Return Book","Active Borrows"])

    with tab1:
        members = get_active_members()
        books   = fetch_all("SELECT Book_ID, Title FROM books WHERE Available_Copies>0")
        if not members or not books:
            st.warning("No active members or available books.")
        else:
            mem_map  = {f"[{m['Member_ID']}] {m['Full_Name']}": m["Member_ID"] for m in members}
            book_map = {f"[{b['Book_ID']}] {b['Title']}": b["Book_ID"] for b in books}
            with st.form("borrow_form", clear_on_submit=True):
                sel_m = st.selectbox("Member", list(mem_map.keys()))
                sel_b = st.selectbox("Book",   list(book_map.keys()))
                due   = st.date_input("Due Date", value=date.today()+timedelta(days=14))
                if st.form_submit_button("Issue Book"):
                    borrow_book(mem_map[sel_m], book_map[sel_b], due)

    with tab2:
        bid = st.number_input("Borrow ID", min_value=1, step=1)
        if st.button("Return Book"):
            return_book(int(bid))

    with tab3:
        df = get_active_borrows()
        if df.empty:
            st.success("No active borrows!")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            