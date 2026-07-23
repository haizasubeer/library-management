import streamlit as st
from db import test_connection, get_kpis
from books import render_books_page
from members import render_members_page
from borrow import render_borrow_page
from reports import render_reports_page

st.set_page_config(page_title="Library MS", page_icon="📚", layout="wide")

# Glowing Colorful CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

/* Dark space theme background */
.stApp {
    background: radial-gradient(circle at 20% 30%, #100b26 0%, #090615 50%, #030209 100%) !important;
    color: #e2e8f0 !important;
}

/* Sidebar with neon border */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0a22 0%, #070513 100%) !important;
    border-right: 2px solid #ff007f !important;
    box-shadow: 5px 0 25px rgba(255, 0, 127, 0.15);
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Gradient Header */
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

/* Metric boxes */
.metric-box {
    text-align: center;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease;
}
.metric-box:hover {
    transform: scale(1.05);
}
.m-pink {
    background: linear-gradient(135deg, rgba(255, 0, 127, 0.15) 0%, rgba(255, 0, 127, 0.05) 100%);
    border-left: 5px solid #ff007f;
}
.m-blue {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.15) 0%, rgba(0, 240, 255, 0.05) 100%);
    border-left: 5px solid #00f0ff;
}
.m-violet {
    background: linear-gradient(135deg, rgba(127, 0, 255, 0.15) 0%, rgba(127, 0, 255, 0.05) 100%);
    border-left: 5px solid #7f00ff;
}
.m-green {
    background: linear-gradient(135deg, rgba(57, 255, 20, 0.15) 0%, rgba(57, 255, 20, 0.05) 100%);
    border-left: 5px solid #39ff14;
}
.m-yellow {
    background: linear-gradient(135deg, rgba(255, 234, 0, 0.15) 0%, rgba(255, 234, 0, 0.05) 100%);
    border-left: 5px solid #ffea00;
}

.m-val {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
}
.m-lbl {
    font-size: 0.85rem;
    font-weight: 600;
    color: #cbd5e0;
    text-transform: uppercase;
    letter-spacing: 1px;
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
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255, 0, 127, 0.7) !important;
}

/* Styled Inputs */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border-radius: 14px;
    padding: 6px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #ff007f, #7f00ff) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
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

    # CSV Database Status Indicator
    st.markdown("""
    <div style='text-align:center; background: linear-gradient(90deg, #0f3014, #1b5e20);
                border: 1px solid #38ef7d; border-radius: 12px; padding: 10px; margin-bottom: 15px;
                font-weight: 700; font-size: 0.85rem; color: #38ef7d;'>
        🟢 Connected to CSV Engine
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    page = st.radio("Navigation Menu", [
        "🏠 Home Dashboard",
        "📚 Books Management",
        "👥 Members Management",
        "📖 Borrow & Return",
        "📊 Reports & Analytics"
    ])

# Page Routing
if page == "🏠 Home Dashboard":
    st.markdown("<h1 class='gradient-header'>📚 Library Management System</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-banner'>Interactive digital space for library administration and performance reports.</p>", unsafe_allow_html=True)

    kpis = get_kpis()

    # Metric Columns
    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
    
    with col_kpi1:
        st.markdown(f"""
        <div class='metric-box m-pink'>
            <div class='m-val' style='color:#ff007f;'>{kpis['total_books']}</div>
            <div class='m-lbl'>📘 Total Books</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi2:
        st.markdown(f"""
        <div class='metric-box m-blue'>
            <div class='m-val' style='color:#00f0ff;'>{kpis['available']}</div>
            <div class='m-lbl'>🟢 Available</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi3:
        st.markdown(f"""
        <div class='metric-box m-violet'>
            <div class='m-val' style='color:#7f00ff;'>{kpis['members']}</div>
            <div class='m-lbl'>👥 Members</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi4:
        st.markdown(f"""
        <div class='metric-box m-green'>
            <div class='m-val' style='color:#39ff14;'>{kpis['borrowed']}</div>
            <div class='m-lbl'>📙 On Loan</div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi5:
        st.markdown(f"""
        <div class='metric-box m-yellow'>
            <div class='m-val' style='color:#ffea00;'>{kpis['overdue']}</div>
            <div class='m-lbl'>⚠️ Overdue</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # Highlighted Fine Collection Box
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #ffea00, #ff9f00);
                border-radius: 16px; padding: 20px 30px;
                box-shadow: 0 10px 35px rgba(255, 234, 0, 0.2);
                display: flex; align-items: center; justify-content: space-between;'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <span style='font-size: 2.8rem;'>💰</span>
            <div>
                <h3 style='margin: 0; color: #0d0d1e; font-size: 1.8rem; font-weight:800;'>₹{kpis['fines']:,.2f}</h3>
                <p style='margin: 0; color: #3a3a5e; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;'>Total Library Fines Collected</p>
            </div>
        </div>
        <div style='background: rgba(0, 0, 0, 0.08); border-radius: 10px; padding: 8px 15px; font-weight: 700; color: #0d0d1e; font-size: 0.9rem;'>
            Auto-calculated: ₹5.00/day
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)

    # Feature Guides
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px; border-top:4px solid #ff007f;'>
            <h3 style='color:#ff007f; margin:0 0 10px 0;'>📚 Inventory System</h3>
            <p style='color:#cbd5e0; font-size:0.9rem; line-height:1.6;'>Search, view, and add books directly to your CSV database. Track titles, authors, categories, and live available stock.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_m2:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px; border-top:4px solid #00f0ff;'>
            <h3 style='color:#00f0ff; margin:0 0 10px 0;'>👥 Patron Directory</h3>
            <p style='color:#cbd5e0; font-size:0.9rem; line-height:1.6;'>Register new members with tier selection (Standard, Premium, Student) and manage active library accounts.</p>
        </div>
        """, unsafe_allow_html=True)
    with c_m3:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px; border-top:4px solid #7f00ff;'>
            <h3 style='color:#7f00ff; margin:0 0 10px 0;'>📖 Circulation Ledger</h3>
            <p style='color:#cbd5e0; font-size:0.9rem; line-height:1.6;'>Process checkouts and returns. Fines are calculated automatically at ₹5/day for late returns.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    if kpis['overdue'] > 0:
        st.error(f"🚨 Attention Required: There are currently {kpis['overdue']} overdue books that need check-in.")
    else:
        st.success("✨ Excellent! All borrowed inventory items are currently in-schedule and healthy.")

elif page == "📚 Books Management":
    render_books_page()

elif page == "👥 Members Management":
    render_members_page()

elif page == "📖 Borrow & Return":
    render_borrow_page()

elif page == "📊 Reports & Analytics":
    render_reports_page()