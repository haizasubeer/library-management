# 📚 Library Management System (CSV Powered)

A complete, full-stack **Library Management System** built with **Python, Pandas, Streamlit, and Plotly**. 

This system features a **zero-dependency, serverless CSV database engine** designed to run seamlessly both locally and on **Streamlit Community Cloud** with 24/7 global access across any device.

---

## ✨ Features

- **🏠 Interactive Home Dashboard:** Real-time KPI metrics showing Total Books, Available Stock, Active Members, Active Borrows, Overdue Items, and Total Fine Collection.
- **📚 Books Management:** Search, view, and add new books to the inventory. Loaded with **100+ book titles** across 11 diverse categories (*Chemistry, Astronomy, Philosophy, Psychology, Art & Design, Mystery, Historical Fiction, Romance, Horror, Adventure, Folk Tales*).
- **👥 Members Directory:** Register new patrons and manage member records with tier classifications (*Standard, Premium, Student*) and status checks (*Active, Inactive, Suspended*). Pre-populated with **25 active member profiles**.
- **📖 Circulation Ledger:** Issue book checkouts and process return check-ins. Features **automatic overdue fine calculation** (₹5.00/day for late returns) and dynamic stock adjustment.
- **📊 Reports & Analytics:** Data visualizations powered by Plotly, including **Top Borrowed Books (Horizontal Bar Chart)** and **Category Concentration (Donut Chart)**.

---

## 🛠️ Technology Stack

| Component | Technology Used |
| :--- | :--- |
| **Language** | Python 3.12+ |
| **Web Framework** | Streamlit |
| **Data Engine** | Pandas (CSV Database Layer) |
| **Charts & Analytics** | Plotly Express |
| **Deployment** | Streamlit Community Cloud |

---

## 📂 Project Structure

```
project 2/
│
├── app/
│   ├── app.py              # Main Streamlit web application & UI router
│   ├── db.py               # CSV Data Access Layer (Pandas)
│   ├── books.py            # Inventory management module
│   ├── members.py          # Member directory module
│   ├── borrow.py           # Circulation & checkout ledger module
│   ├── reports.py          # Analytics & Plotly charts module
│   ├── books.csv           # Books database file (100+ records)
│   ├── members.csv         # Members database file (25 records)
│   └── borrow_records.csv  # Transaction records & fine tracking
│
├── database/
│   ├── library.sql         # Original SQL schema reference
│   └── datas.sql           # Original sample data reference
│
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Run Locally on your PC

1. **Clone or download** this project folder to your computer.
2. Open **Command Prompt** or **PowerShell** inside the project folder:
   ```bash
   cd "C:\Users\USER\OneDrive\Desktop\project 2"
   ```
3. Run the application:
   ```bash
   python -m streamlit run app/app.py
   ```
4. Open your browser to **`http://localhost:8501`**.

---

### 2. Deploy to Streamlit Cloud (24/7 Live Online Access)

To make your project accessible to anyone on any device:

1. Push this project repository to **GitHub**.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
3. Click **New App**, select your GitHub repository, set Main file path to **`app/app.py`**, and click **Deploy**.

Your live URL (`https://...streamlit.app`) will be active globally!

---

## 📄 License & Credits

Designed & developed for internship Project & Portfolio demonstration.
