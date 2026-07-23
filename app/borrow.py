import streamlit as st
import pandas as pd
from datetime import date, timedelta
from db import get_books_df, save_books_df, get_members_df, get_borrow_df, save_borrow_df

FINE_PER_DAY = 5.00

def borrow_book(member_id, book_id, due_date):
    books_df = get_books_df()
    members_df = get_members_df()
    borrow_df = get_borrow_df()

    # Validate Member
    member = members_df[members_df["Member_ID"] == member_id]
    if member.empty or member.iloc[0]["Status"] != "Active":
        st.error("❌ Selected member is not found or not Active.")
        return False

    # Validate Book
    book_idx = books_df[books_df["Book_ID"] == book_id].index
    if len(book_idx) == 0:
        st.error("❌ Book not found.")
        return False

    avail = int(books_df.loc[book_idx[0], "Available_Copies"])
    if avail < 1:
        st.error("❌ Selected book has zero available copies left.")
        return False

    # Update copies in books dataframe
    books_df.loc[book_idx[0], "Available_Copies"] = avail - 1
    save_books_df(books_df)

    # Append borrow record
    new_id = int(borrow_df["Borrow_ID"].max() + 1) if not borrow_df.empty and len(borrow_df) > 0 else 1

    new_record = {
        "Borrow_ID": new_id,
        "Member_ID": int(member_id),
        "Book_ID": int(book_id),
        "Borrow_Date": str(date.today()),
        "Due_Date": str(due_date),
        "Return_Date": "",
        "Fine_Amount": 0.0,
        "Borrow_Status": "Borrowed"
    }

    borrow_df = pd.concat([borrow_df, pd.DataFrame([new_record])], ignore_index=True)
    save_borrow_df(borrow_df)

    book_title = books_df.loc[book_idx[0], "Title"]
    member_name = member.iloc[0]["Full_Name"]
    st.success(f"🎉 Book '{book_title}' issued successfully to {member_name}!")
    return True

def return_book(borrow_id):
    books_df = get_books_df()
    borrow_df = get_borrow_df()

    rec_idx = borrow_df[borrow_df["Borrow_ID"] == borrow_id].index
    if len(rec_idx) == 0:
        st.error("❌ Borrow Record ID not found.")
        return False

    record = borrow_df.loc[rec_idx[0]]
    if record["Borrow_Status"] == "Returned":
        st.warning("⚠️ This record is already marked as Returned.")
        return False

    # Calculate fine
    today = date.today()
    due_dt = date.fromisoformat(str(record["Due_Date"]))
    fine = 0.0
    if today > due_dt:
        days_late = (today - due_dt).days
        fine = float(days_late * FINE_PER_DAY)

    # Update borrow record
    borrow_df.loc[rec_idx[0], "Return_Date"] = str(today)
    borrow_df.loc[rec_idx[0], "Fine_Amount"] = fine
    borrow_df.loc[rec_idx[0], "Borrow_Status"] = "Returned"
    save_borrow_df(borrow_df)

    # Restore available copy in books
    book_id = int(record["Book_ID"])
    b_idx = books_df[books_df["Book_ID"] == book_id].index
    if len(b_idx) > 0:
        books_df.loc[b_idx[0], "Available_Copies"] = int(books_df.loc[b_idx[0], "Available_Copies"]) + 1
        save_books_df(books_df)

    if fine > 0:
        st.warning(f"✅ Book Returned successfully! Overdue Fine Collected: ₹{fine:.2f}")
    else:
        st.success("✅ Book Returned on time! No fine charged.")
    return True

def render_borrow_page():
    st.markdown("<h2 style='color:#7f00ff;'>📖 Circulation Ledger</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📤 Issue Checkout", "📥 Return Check-in", "📋 Active Transactions"])

    books_df = get_books_df()
    members_df = get_members_df()
    borrow_df = get_borrow_df()

    with tab1:
        active_members = members_df[members_df["Status"] == "Active"]
        avail_books = books_df[books_df["Available_Copies"] > 0]

        if active_members.empty or avail_books.empty:
            st.warning("⚠️ You need at least one Active Member and one Available Book to perform a checkout.")
        else:
            member_map = {f"[{row['Member_ID']}] {row['Full_Name']} ({row['Email']})": row["Member_ID"] for _, row in active_members.iterrows()}
            book_map = {f"[{row['Book_ID']}] {row['Title']} (Avail: {row['Available_Copies']})": row["Book_ID"] for _, row in avail_books.iterrows()}

            with st.form("borrow_form", clear_on_submit=True):
                sel_m = st.selectbox("Select Member *", list(member_map.keys()))
                sel_b = st.selectbox("Select Book *", list(book_map.keys()))
                due_date = st.date_input("Scheduled Return Due Date", value=date.today() + timedelta(days=14))

                if st.form_submit_button("📤 Checkout & Issue Book"):
                    if borrow_book(member_map[sel_m], book_map[sel_b], due_date):
                        st.rerun()

    with tab2:
        active_borrows = borrow_df[borrow_df["Borrow_Status"].isin(["Borrowed", "Overdue"])]
        if active_borrows.empty:
            st.success("✨ All issued books are currently returned! No pending check-ins.")
        else:
            # Join with member and book title for dropdown selection
            borrow_options = {}
            for _, row in active_borrows.iterrows():
                b_title = books_df[books_df["Book_ID"] == row["Book_ID"]]["Title"].values[0] if not books_df[books_df["Book_ID"] == row["Book_ID"]].empty else "Unknown Book"
                m_name = members_df[members_df["Member_ID"] == row["Member_ID"]]["Full_Name"].values[0] if not members_df[members_df["Member_ID"] == row["Member_ID"]].empty else "Unknown Member"
                label = f"ID #{row['Borrow_ID']} | Book: '{b_title}' → Member: {m_name} (Due: {row['Due_Date']})"
                borrow_options[label] = int(row["Borrow_ID"])

            sel_borrow_label = st.selectbox("Select Borrow Transaction to Return", list(borrow_options.keys()))
            
            if st.button("📥 Process Return Check-in"):
                if return_book(borrow_options[sel_borrow_label]):
                    st.rerun()

    with tab3:
        if borrow_df.empty:
            st.info("No borrow records registered.")
        else:
            # Format combined table
            merged = borrow_df.copy()
            merged["Book_Title"] = merged["Book_ID"].apply(
                lambda x: books_df[books_df["Book_ID"] == x]["Title"].values[0] if not books_df[books_df["Book_ID"] == x].empty else "Unknown"
            )
            merged["Member_Name"] = merged["Member_ID"].apply(
                lambda x: members_df[members_df["Member_ID"] == x]["Full_Name"].values[0] if not members_df[members_df["Member_ID"] == x].empty else "Unknown"
            )
            
            display_df = merged[["Borrow_ID", "Member_Name", "Book_Title", "Borrow_Date", "Due_Date", "Return_Date", "Fine_Amount", "Borrow_Status"]]
            st.dataframe(display_df, use_container_width=True, hide_index=True)