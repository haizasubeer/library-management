import mysql.connector
from mysql.connector import Error
import streamlit as st

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "750796",  
    "database": "library_management",
}

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        st.error(f"Connection failed: {e}")
        raise

def execute_query(query, params=()):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Error as e:
        if conn: conn.rollback()
        st.error(f"Query Error: {e}")
        return False
    finally:
        if conn and conn.is_connected(): conn.close()

def fetch_all(query, params=()):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()
    except Error as e:
        st.error(f"Fetch Error: {e}")
        return []
    finally:
        if conn and conn.is_connected(): conn.close()

def fetch_one(query, params=()):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchone()
    except Error as e:
        st.error(f"Fetch Error: {e}")
        return None
    finally:
        if conn and conn.is_connected(): conn.close()

def test_connection():
    try:
        conn = get_connection()
        if conn.is_connected():
            conn.close()
            return True
    except:
        return False