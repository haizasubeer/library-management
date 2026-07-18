import streamlit as st
from db      import test_connection
from books   import render_books_page
from members import render_members_page
from borrow  import render_borrow_page
from reports import render_reports_page, get_kpis
from datetime import date, timedelta

# Initialize Session State
if "db_online" not in st.session_state:
    st.session_state.db_online = False
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

# Quick connection probe
db_status = test_connection()

# If DB is offline, automatically enable Demo Mode
if not db_status:
    st.session_state.demo_mode = True

# ── Self-Contained Mock Database Engine ────────────────────────
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
        today_date = date.today()
        st.session_state.mock_borrows = [
            {"Borrow_ID": 1, "Member_ID": 1, "Book_ID": 1, "Borrow_Date": today_date - timedelta(days=10), "Due_Date": today_date + timedelta(days=4), "Return_Date": None, "Fine_Amount": 0.0, "Borrow_Status": "Borrowed"},
            {"Borrow_ID": 2, "Member_ID": 2, "Book_ID": 2, "Borrow_Date": today_date - timedelta(days=20), "Due_Date": today_date - timedelta(days=6), "Return_Date": None, "Fine_Amount": 30.0, "Borrow_Status": "Overdue"},
            {"Borrow_ID": 3, "Member_ID": 3, "Book_ID": 5, "Borrow_Date": today_date - timedelta(days=15), "Due_Date": today_date - timedelta(days=1), "Return_Date": today_date, "Fine_Amount": 5.0, "Borrow_Status": "Returned"},
            {"Borrow_ID": 4, "Member_ID": 4, "Book_ID": 9, "Borrow_Date": today_date - timedelta(days=5), "Due_Date": today_date + timedelta(days=9), "Return_Date": None, "Fine_Amount": 0.0, "Borrow_Status": "Borrowed"}
        ]

def get_cat_name(cat_id):
    for c in st.session_state.mock_categories:
        if c["Category_ID"] == cat_id:
            return c["Category_Name"]
    return "Unknown"

def mock_get_all_books():
    init_mock_data()
    books = []
    for b in st.session_state.mock_books:
        bk = b.copy()
        bk["Category"] = get_cat_name(b["Category_ID"])
        books.append(bk)
    import pandas as pd
    df = pd.DataFrame(books)
    if not df.empty:
        df = df[["Book_ID", "ISBN", "Title", "Author", "Category", "Total_Copies", "Available_Copies", "Shelf_Number"]]
    return df

def mock_add_book(isbn, title, author, category_id, publisher, year, total, available, shelf):
    init_mock_data()
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

def mock_get_all_members():
    init_mock_data()
    import pandas as pd
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
    import pandas as pd
    return pd.DataFrame(borrows)

def mock_borrow_book(member_id, book_id, due_date):
    init_mock_data()
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
            
            for b in st.session_state.mock_books:
                if b["Book_ID"] == br["Book_ID"]:
                    b["Available_Copies"] += 1
            
            today_val = date.today()
            due = br["Due_Date"]
            fine = max(0, (today_val - due).days) * 5.00 if today_val > due else 0.0
            
            br["Return_Date"] = today_val
            br["Fine_Amount"] = fine
            br["Borrow_Status"] = "Returned"
            
            if fine > 0:
                st.warning(f"Returned! Fine: ₹{fine:.2f} (Demo Mode)")
            else:
                st.success("Returned on time. No fine. (Demo Mode)")
            return True
            
    st.error("Borrow ID not found in Demo Mode.")
    return False

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
    counts = {1: 15, 2: 12, 5: 25, 9: 18}
    rows = []
    for b in st.session_state.mock_books:
        bid = b["Book_ID"]
        if bid in counts:
            rows.append({"Title": b["Title"], "Borrows": counts[bid]})
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

# If in demo mode, initialize it
if st.session_state.demo_mode:
    init_mock_data()


st.set_page_config(page_title="Library MS", page_icon="📚", layout="wide")

# ── Glowing Colorful CSS Styling ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

/* Overall dark space theme background */
.stApp {
    background: radial-gradient(circle at 20% 30%, #100b26 0%, #090615 50%, #030209 100%) !important;
    color: #e2e8f0 !important;
}

/* Sidebar with neon gradient border */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0a22 0%, #070513 100%) !important;
    border-right: 2px solid #ff007f !important;
    box-shadow: 5px 0 25px rgba(255, 0, 127, 0.15);
}

/* Sidebar elements */
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Beautiful custom headers with gradients */
.gradient-header {
    background: linear-gradient(90deg, #ff007f, #7f00ff, #00f0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 2.8rem;
    margin-bottom: 0.2rem;
}

.sub-banner {
    color: #a0aec0;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Custom interactive card wrapper */
.glow-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    margin-bottom: 20px;
    transition: transform 0.3s ease, border 0.3s ease, box-shadow 0.3s ease;
}

.glow-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(255, 0, 127, 0.5);
    box-shadow: 0 15px 40px rgba(255, 0, 127, 0.25);
}

/* Custom metric panels */
.metric-box {
    text-align: center;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.metric-box:hover {
    transform: scale(1.05);
}
.m-pink {
    background: linear-gradient(135deg, rgba(255, 0, 127, 0.15) 0%, rgba(255, 0, 127, 0.05) 100%);
    border-left: 5px solid #ff007f;
    box-shadow: 0 8px 30px rgba(255, 0, 127, 0.2);
}
.m-blue {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.15) 0%, rgba(0, 240, 255, 0.05) 100%);
    border-left: 5px solid #00f0ff;
    box-shadow: 0 8px 30px rgba(0, 240, 255, 0.2);
}
.m-violet {
    background: linear-gradient(135deg, rgba(127, 0, 255, 0.15) 0%, rgba(127, 0, 255, 0.05) 100%);
    border-left: 5px solid #7f00ff;
    box-shadow: 0 8px 30px rgba(127, 0, 255, 0.2);
}
.m-green {
    background: linear-gradient(135deg, rgba(57, 255, 20, 0.15) 0%, rgba(57, 255, 20, 0.05) 100%);
    border-left: 5px solid #39ff14;
    box-shadow: 0 8px 30px rgba(57, 255, 20, 0.2);
}
.m-yellow {
    background: linear-gradient(135deg, rgba(255, 234, 0, 0.15) 0%, rgba(255, 234, 0, 0.05) 100%);
    border-left: 5px solid #ffea00;
    box-shadow: 0 8px 30px rgba(255, 234, 0, 0.2);
}

.m-val {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
    text-shadow: 0 0 10px rgba(255,255,255,0.2);
}
.m-lbl {
    font-size: 0.85rem;
    font-weight: 600;
    color: #cbd5e0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Custom styled inputs and selectboxes */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: white !important;
    border-radius: 12px !important;
    transition: all 0.3s ease;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: #ff007f !important;
    box-shadow: 0 0 10px rgba(255, 0, 127, 0.4) !important;
}

/* Custom gorgeous buttons */
.stButton > button {
    background: linear-gradient(90deg, #ff007f 0%, #7f00ff 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 0.6rem 2.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 0, 127, 0.4) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255, 0, 127, 0.7) !important;
    background: linear-gradient(90deg, #ff007f 0%, #00f0ff 100%) !important;
}

/* Tabs customization */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border-radius: 14px;
    padding: 6px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    color: #a0aec0 !important;
    font-weight: 600;
    border-radius: 10px;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #ff007f, #7f00ff) !important;
    color: white !important;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    background-color: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 25px 0 15px;'>
        <div style='font-size: 4.5rem; text-shadow: 0 0 15px rgba(255, 0, 127, 0.5);'>📚</div>
        <div style='font-size: 1.6rem; font-weight: 800; letter-spacing: 1.5px;
                    background: linear-gradient(90deg, #ff007f, #7f00ff, #00f0ff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;'>
            LibraryMS
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Connection Status Indicator
    if db_status:
        st.markdown("""
        <div style='text-align:center; background: linear-gradient(90deg, #0f3014, #1b5e20);
                    border: 1px solid #38ef7d; border-radius: 12px; padding: 8px; margin-bottom: 15px;
                    font-weight: 700; font-size: 0.85rem; color: #38ef7d;'>
            🟢 Connected to Local MySQL
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center; background: linear-gradient(90deg, #3d0c11, #b71c1c);
                    border: 1px solid #ff4d4d; border-radius: 12px; padding: 8px; margin-bottom: 15px;
                    font-weight: 700; font-size: 0.85rem; color: #ff4d4d;'>
            🔴 MySQL server offline
        </div>
        """, unsafe_allow_html=True)
        
    # Interactive Toggle Mode
    st.session_state.demo_mode = st.toggle("🚀 Active Demo Mode (Interactive)", value=st.session_state.demo_mode)
    
    if st.session_state.demo_mode:
        st.info("💡 Running in interactive DEMO MODE with mockup memory. You can add, return, and borrow books live in your browser!")

    st.markdown("---")
    
    page = st.radio("Navigation Menu", [
        "🏠 Home Dashboard",
        "📚 Books Management",
        "👥 Members Management",
        "📖 Borrow & Return",
        "📊 Reports & Analytics"
    ])

# Fetch KPIs
if st.session_state.demo_mode:
    kpis = mock_get_kpis()
else:
    kpis = get_kpis()

total_books = kpis.get("total_books", 0)
available   = kpis.get("available", 0)
members     = kpis.get("members", 0)
borrowed    = kpis.get("borrowed", 0)
overdue     = kpis.get("overdue", 0)
fines       = kpis.get("fines", 0)

# ── Page Routing ──────────────────────────────────────────────
if page == "🏠 Home Dashboard":
    st.markdown("<h1 class='gradient-header'>📚 Library Management System</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-banner'>Interactive digital space for library administration and performance reports.</p>", unsafe_allow_html=True)

    # Glowing Colorful Metric Column cards
    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
    
    with col_kpi1:
        st.markdown(f"""
        <div class='metric-box m-pink'>
            <div class='m-val' style='color:#ff007f;'>{total_books}</div>
            <div class='m-lbl'>📘 Total Books</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi2:
        st.markdown(f"""
        <div class='metric-box m-blue'>
            <div class='m-val' style='color:#00f0ff;'>{available}</div>
            <div class='m-lbl'>🟢 Available</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi3:
        st.markdown(f"""
        <div class='metric-box m-violet'>
            <div class='m-val' style='color:#7f00ff;'>{members}</div>
            <div class='m-lbl'>👥 Members</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi4:
        st.markdown(f"""
        <div class='metric-box m-green'>
            <div class='m-val' style='color:#39ff14;'>{borrowed}</div>
            <div class='m-lbl'>📙 On Loan</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi5:
        st.markdown(f"""
        <div class='metric-box m-yellow'>
            <div class='m-val' style='color:#ffea00;'>{overdue}</div>
            <div class='m-lbl'>⚠️ Overdue</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # Highlighted Fine Collection box
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #ffea00, #ff9f00);
                border-radius: 16px; padding: 20px 30px;
                box-shadow: 0 10px 35px rgba(255, 234, 0, 0.2);
                display: flex; align-items: center; justify-content: space-between;'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <span style='font-size: 2.8rem;'>💰</span>
            <div>
                <h3 style='margin: 0; color: #0d0d1e; font-size: 1.8rem; font-weight:800;'>₹{float(fines):,.2f}</h3>
                <p style='margin: 0; color: #3a3a5e; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;'>Total Library Fines Collected</p>
            </div>
        </div>
        <div style='background: rgba(0, 0, 0, 0.08); border-radius: 10px; padding: 8px 15px; font-weight: 700; color: #0d0d1e; font-size: 0.9rem;'>
            Auto-calculated: ₹5.00/day
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)

    # Beautiful module guide columns
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown("""
        <div class='glow-card' style='border-top: 4px solid #ff007f;'>
            <h3 style='color:#ff007f; margin:0 0 10px 0;'>📚 Inventory System</h3>
            <p style='color:#cbd5e0; font-size:0.9rem; line-height:1.6;'>Manage entire library titles, ISBNs, authors, publishers, shelf codes, and edit available stock seamlessly.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_m2:
        st.markdown("""
        <div class='glow-card' style='border-top: 4px solid #00f0ff;'>
            <h3 style='color:#00f0ff; margin:0 0 10px 0;'>👥 Patron Directory</h3>
            <p style='color:#cbd5e0; font-size:0.9rem; line-height:1.6;'>Track active readers, register new accounts with specific membership types (Standard, Premium, Student) and status check.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_m3:
        st.markdown("""
        <div class='glow-card' style='border-top: 4px solid #7f00ff;'>
            <h3 style='color:#7f00ff; margin:0 0 10px 0;'>📖 Circulation Ledger</h3>
            <p style='color:#cbd5e0; font-size:0.9rem; line-height:1.6;'>Run book checkouts and return check-ins. Fines are calculated automatically by dates and copies are adjusted live.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    if overdue > 0:
        st.error(f"🚨 Urgent Attention Required: There are currently {overdue} overdue books that need immediate check-in.")
    else:
        st.success("✨ Excellent! All borrowed inventory items are currently in-schedule and healthy.")

elif page == "📚 Books Management":
    if st.session_state.demo_mode:
        # Override render books page with mock data
        st.markdown("<h2 style='color:#ff007f;'>📚 Books Management (Demo Mode)</h2>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📋 View Book Inventory", "➕ Add New Book"])
        with tab1:
            df = mock_get_all_books()
            if df.empty: st.info("No books found.")
            else: st.dataframe(df, use_container_width=True, hide_index=True)
        with tab2:
            with st.form("demo_add_book_form", clear_on_submit=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    isbn = st.text_input("ISBN Code *", placeholder="e.g. 978-0134685991")
                    title = st.text_input("Title *")
                    author = st.text_input("Author *")
                with col_b:
                    cats = st.session_state.mock_categories
                    cat_map = {c["Category_Name"]: c["Category_ID"] for c in cats}
                    cat = st.selectbox("Category", list(cat_map.keys()))
                    total = st.number_input("Total copies", 1, 100, 5)
                    shelf = st.text_input("Shelf location", placeholder="e.g. CS-C3")
                if st.form_submit_button("Add Book"):
                    mock_add_book(isbn, title, author, cat_map[cat], "Publisher", 2024, total, total, shelf)
    else:
        render_books_page()

elif page == "👥 Members Management":
    if st.session_state.demo_mode:
        st.markdown("<h2 style='color:#00f0ff;'>👥 Members Directory (Demo Mode)</h2>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📋 Active Directory", "➕ Add New Member"])
        with tab1:
            df = mock_get_all_members()
            st.dataframe(df, use_container_width=True, hide_index=True)
        with tab2:
            with st.form("demo_add_member", clear_on_submit=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    name = st.text_input("Full Name *")
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                    email = st.text_input("Email *")
                with col_b:
                    phone = st.text_input("Phone Number *")
                    mtype = st.selectbox("Membership Type", ["Standard", "Premium", "Student"])
                    status = st.selectbox("Status", ["Active", "Inactive"])
                if st.form_submit_button("Register Member"):
                    mock_add_member(name, gender, email, phone, "Address details", mtype, status)
    else:
        render_members_page()

elif page == "📖 Borrow & Return":
    if st.session_state.demo_mode:
        st.markdown("<h2 style='color:#7f00ff;'>📖 Circulation Ledger (Demo Mode)</h2>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["📤 Issue Checkout", "📥 Return Check-in", "📋 Active Transactions"])
        
        with tab1:
            m_list = mock_get_active_members()
            b_list = st.session_state.mock_books
            avail_b = [b for b in b_list if b["Available_Copies"] > 0]
            
            if not m_list or not avail_b:
                st.warning("No active members or books with available copies found.")
            else:
                m_map = {f"[{m['Member_ID']}] {m['Full_Name']}": m["Member_ID"] for m in m_list}
                b_map = {f"[{b['Book_ID']}] {b['Title']}": b["Book_ID"] for b in avail_b}
                with st.form("demo_borrow_form", clear_on_submit=True):
                    sel_m = st.selectbox("Member ID", list(m_map.keys()))
                    sel_b = st.selectbox("Book ID", list(b_map.keys()))
                    due = st.date_input("Due Date Return", value=date.today() + timedelta(days=14))
                    if st.form_submit_button("Checkout Book"):
                        mock_borrow_book(m_map[sel_m], b_map[sel_b], due)
        with tab2:
            bid = st.number_input("Enter Transaction ID to Return", min_value=1, step=1)
            if st.button("Complete Return Check-in"):
                mock_return_book(int(bid))
        with tab3:
            df = mock_get_active_borrows()
            if df.empty: st.success("Clear transaction list!")
            else: st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        render_borrow_page()

elif page == "📊 Reports & Analytics":
    if st.session_state.demo_mode:
        import plotly.express as px
        import pandas as pd
        st.markdown("<h2 style='color:#ffea00;'>📊 Reports & Performance (Demo Mode)</h2>", unsafe_allow_html=True)
        
        # Display charts
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            rows = mock_get_most_borrowed_books()
            if rows:
                df_b = pd.DataFrame(rows)
                fig_b = px.bar(df_b, x="Borrows", y="Title", orientation="h",
                               title="🥇 Top Borrowed Books",
                               color="Borrows", color_continuous_scale="Plasma")
                fig_b.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                st.plotly_chart(fig_b, use_container_width=True)
                
        with col_c2:
            rows2 = mock_get_books_by_category()
            if rows2:
                df_c = pd.DataFrame(rows2)
                fig_c = px.pie(df_c, names="Category", values="Books",
                               title="📦 Category Concentration",
                               hole=0.4, color_discrete_sequence=px.colors.sequential.Sunsetdark)
                fig_c.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                st.plotly_chart(fig_c, use_container_width=True)
    else:
        render_reports_page()