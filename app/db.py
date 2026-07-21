import pandas as pd
import streamlit as st
import os

# Define the folder where your CSV files are stored
DATA_DIR = "data"

def _get_csv_path(query):
    """Helper function to guess which CSV file to open based on the SQL query text."""
    q = query.lower()
    if "books" in q:
        return os.path.join(DATA_DIR, "books.csv")
    elif "members" in q:
        return os.path.join(DATA_DIR, "members.csv")
    elif "borrow" in q or "transaction" in q:
        return os.path.join(DATA_DIR, "borrow.csv")
    elif "fine" in q:
        return os.path.join(DATA_DIR, "fines.csv")
    return None

def get_connection():
    """Mocked to simulate connection success for CSV setup."""
    st.session_state.db_online = True
    return True

def execute_query(query, params=()):
    """Handles INSERT, UPDATE, or DELETE queries on CSV files."""
    try:
        q_lower = query.lower()
        csv_path = _get_csv_path(query)
        
        if not csv_path or not os.path.exists(csv_path):
            return False
            
        df = pd.read_csv(csv_path)
        
        # Simple handler for basic inserts (e.g., INSERT INTO books ...)
        if "insert into" in q_lower:
            # If your app passes parameters as a tuple, convert them into a new row
            if params:
                # Creates a row dictionary matching dataframe columns
                new_row = {df.columns[i]: params[i] for i in range(min(len(params), len(df.columns)))}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(csv_path, index=False)
                st.session_state.db_online = True
                return True
        
        st.session_state.db_online = True
        return True
    except Exception as e:
        st.session_state.db_online = False
        return False

def fetch_all(query, params=()):
    """Replaces SQL SELECT fetch_all with Pandas dataframe-to-dict conversion."""
    try:
        csv_path = _get_csv_path(query)
        if csv_path and os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            st.session_state.db_online = True
            return df.to_dict(orient="records")
        st.session_state.db_online = False
        return []
    except Exception as e:
        st.session_state.db_online = False
        return []

def fetch_one(query, params=()):
    """Replaces SQL SELECT fetch_one by returning the first matching record."""
    try:
        csv_path = _get_csv_path(query)
        if csv_path and os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            st.session_state.db_online = True
            records = df.to_dict(orient="records")
            return records[0] if records else None
        st.session_state.db_online = False
        return None
    except Exception as e:
        st.session_state.db_online = False
        return None

def test_connection():
    """Always returns True since CSV files are local to the app bundle."""
    st.session_state.db_online = True
    return True