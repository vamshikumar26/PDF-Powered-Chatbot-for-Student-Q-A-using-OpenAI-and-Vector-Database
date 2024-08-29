import streamlit as st
from db import create_connection
import mysql
def register_page(switch_page):
    st.title("Register Page")
    
    username = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if password == confirm_password:
            conn = create_connection()
            cursor = conn.cursor()
            
            try:
                if "@" in username:
                    cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                else:
                    cursor.execute("INSERT INTO students(username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                st.success("Account created successfully!")
                
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                conn.close()
            switch_page('Login')
        else:
            st.error("Passwords do not match.")
    
    if st.button("Back to Login"):
        switch_page('Login')
