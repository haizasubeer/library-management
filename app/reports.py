"""
==============================================================
 Library Management System
 File        : reports.py
 Description : Analytics & Visualization module using Plotly & CSV.
==============================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_books_df, get_borrow_df, get_kpis

def render_reports_page():
    st.markdown("<h2 style='color:#ffea00;'>📊 Reports & Analytics</h2>", unsafe_allow_html=True)
    
    kpis = get_kpis()
    
    # Display 5 KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📘 Total Books", kpis["total_books"])
    col2.metric("🟢 Available", kpis["available"])
    col3.metric("👥 Active Members", kpis["members"])
    col4.metric("📙 On Loan", kpis["borrowed"])
    col5.metric("⚠️ Overdue", kpis["overdue"])

    st.markdown("---")

    books_df = get_books_df()
    borrow_df = get_borrow_df()

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("🥇 Top Borrowed Books")
        if not borrow_df.empty and not books_df.empty:
            merged = borrow_df.merge(books_df, on="Book_ID", how="inner")
            counts = merged["Title"].value_counts().reset_index()
            counts.columns = ["Title", "Borrows"]
            counts = counts.head(10)

            fig_bar = px.bar(
                counts, x="Borrows", y="Title", orientation="h",
                color="Borrows", color_continuous_scale="Plasma"
            )
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Insufficient borrow history data to plot chart.")

    with col_chart2:
        st.subheader("📦 Category Distribution")
        if not books_df.empty:
            cat_counts = books_df["Category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]

            fig_pie = px.pie(
                cat_counts, names="Category", values="Count",
                hole=0.4, color_discrete_sequence=px.colors.sequential.Sunsetdark
            )
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No category data found in books inventory.")

    st.markdown("---")
    st.subheader(f"💰 Total Library Fines Collected: ₹{kpis['fines']:,.2f}")