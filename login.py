import streamlit as st
from db import create_connection
import student
import admin
import chat
import studentchat
def login_admin(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def login_student(roll_number, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE username = %s AND password = %s", (roll_number, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
def login_page(switch_page):
    st.title("Login Page")
    
    user_identifier = st.text_input("Roll Number or Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if "@" in user_identifier:  
            is_admin = login_admin(user_identifier, password)
            if is_admin:
                st.success("Admin identified")
                switch_page('chat')
            else:
                st.error("Invalid admin credentials")
        else:
            is_student = login_student(user_identifier, password)
            if is_student:
                st.success("Student identified")
                switch_page('studentchat')
            else:
                st.error("Invalid student credentials")

    if st.button("Forgot Password?"):
        st.write("Password recovery is not implemented yet.")
    
    if st.button("Don't have an account? Register here"):
        switch_page('Register')
