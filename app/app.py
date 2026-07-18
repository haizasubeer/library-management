import streamlit as st
from db      import test_connection
from books   import render_books_page
from members import render_members_page
from borrow  import render_borrow_page
from reports import render_reports_page, get_kpis

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

# Import mock engine if in demo mode
if st.session_state.demo_mode:
    import mock_data
    mock_data.init_mock_data()

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
    kpis = mock_data.mock_get_kpis()
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
            df = mock_data.mock_get_all_books()
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
                    cats = mock_data.st.session_state.mock_categories
                    cat_map = {c["Category_Name"]: c["Category_ID"] for c in cats}
                    cat = st.selectbox("Category", list(cat_map.keys()))
                    total = st.number_input("Total copies", 1, 100, 5)
                    shelf = st.text_input("Shelf location", placeholder="e.g. CS-C3")
                if st.form_submit_button("Add Book"):
                    mock_data.mock_add_book(isbn, title, author, cat_map[cat], "Publisher", 2024, total, total, shelf)
    else:
        render_books_page()

elif page == "👥 Members Management":
    if st.session_state.demo_mode:
        st.markdown("<h2 style='color:#00f0ff;'>👥 Members Directory (Demo Mode)</h2>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📋 Active Directory", "➕ Add New Member"])
        with tab1:
            df = mock_data.mock_get_all_members()
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
                    mock_data.mock_add_member(name, gender, email, phone, "Address details", mtype, status)
    else:
        render_members_page()

elif page == "📖 Borrow & Return":
    if st.session_state.demo_mode:
        st.markdown("<h2 style='color:#7f00ff;'>📖 Circulation Ledger (Demo Mode)</h2>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["📤 Issue Checkout", "📥 Return Check-in", "📋 Active Transactions"])
        
        with tab1:
            m_list = mock_data.mock_get_active_members()
            b_list = mock_data.st.session_state.mock_books
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
                        mock_data.mock_borrow_book(m_map[sel_m], b_map[sel_b], due)
        with tab2:
            bid = st.number_input("Enter Transaction ID to Return", min_value=1, step=1)
            if st.button("Complete Return Check-in"):
                mock_data.mock_return_book(int(bid))
        with tab3:
            df = mock_data.mock_get_active_borrows()
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
            rows = mock_data.mock_get_most_borrowed_books()
            if rows:
                df_b = pd.DataFrame(rows)
                fig_b = px.bar(df_b, x="Borrows", y="Title", orientation="h",
                               title="🥇 Top Borrowed Books",
                               color="Borrows", color_continuous_scale="Plasma")
                fig_b.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                st.plotly_chart(fig_b, use_container_width=True)
                
        with col_c2:
            rows2 = mock_data.mock_get_books_by_category()
            if rows2:
                df_c = pd.DataFrame(rows2)
                fig_c = px.pie(df_c, names="Category", values="Books",
                               title="📦 Category Concentration",
                               hole=0.4, color_discrete_sequence=px.colors.sequential.Sunsetdark)
                fig_c.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
                st.plotly_chart(fig_c, use_container_width=True)
    else:
        render_reports_page()