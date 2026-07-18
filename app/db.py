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
        conn = mysql.connector.connect(**DB_CONFIG)
        st.session_state.db_online = True
        return conn
    except Error as e:
        st.session_state.db_online = False
        raise e

def execute_query(query, params=()):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        st.session_state.db_online = False
        return False
    finally:
        if conn and conn.is_connected(): conn.close()

def fetch_all(query, params=()):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        res = cursor.fetchall()
        return res
    except Exception as e:
        st.session_state.db_online = False
        return []
    finally:
        if conn and conn.is_connected(): conn.close()

def fetch_one(query, params=()):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        res = cursor.fetchone()
        return res
    except Exception as e:
        st.session_state.db_online = False
        return None
    finally:
        if conn and conn.is_connected(): conn.close()

def test_connection():
    try:
        conn = get_connection()
        if conn.is_connected():
            conn.close()
            st.session_state.db_online = True
            return True
    except:
        st.session_state.db_online = False
        return False
    return False