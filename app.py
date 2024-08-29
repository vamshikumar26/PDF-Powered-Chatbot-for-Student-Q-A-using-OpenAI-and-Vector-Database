import streamlit as st
import studentchat
import login
import register
import chat
# Function to switch between pages
def switch_page(page_name):
    st.session_state['page'] = page_name
    
# Initial page state
if 'page' not in st.session_state:
    st.session_state['page'] = 'Login'

# Routing logic based on the selected page
if st.session_state['page'] == 'Login':
    login.login_page(switch_page)
elif st.session_state['page'] == 'Register':
    register.register_page(switch_page)
elif st.session_state['page']=='chat':
    chat.chat_page(switch_page)
elif st.session_state['page']=='studentchat':
    studentchat.chatbot_page(switch_page)
