import mysql.connector

def create_connection():
    conn = mysql.connector.connect(
        host="193.203.184.36",
        user="u786034410_chatbot",  
        password="Chatbot@123$", 
        database="u786034410_chatbot" 
    )
    return conn
