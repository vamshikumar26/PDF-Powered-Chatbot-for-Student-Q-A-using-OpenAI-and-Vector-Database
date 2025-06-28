# 🤖 PDF-Powered Chatbot for Student Q&A using OpenAI and Vector Database

This project is an AI-based chatbot system designed to help students get answers from academic documents (PDFs) uploaded by an admin. The PDFs are converted into embeddings and stored in a vector database, allowing the chatbot to retrieve contextually relevant information when students ask queries. The chatbot uses OpenAI’s language model to generate answers based on these embeddings.

---

## 🧠 Key Features

- Admin can upload one or more academic PDFs
- PDF content is chunked and converted into embeddings
- Embeddings are stored in a vector database (e.g., FAISS etc.)
- Students can ask natural language queries
- OpenAI API retrieves the most relevant chunks and generates an answer

---

## 🗂️ Project Structure
.
├── app.py # Main entry point (router/controller logic)
├── chat.py # Admin: Upload PDFs and store embeddings in vector DB
├── studentchat.py # Student: Ask queries and get responses from chatbot
├── db.py # Stores user info, questions, and answers in a database
├── login.py # Student/admin login functionality
├── register.py # New user registration logic
├── requirements.txt # Python dependencies
└── README.md # You're here!


 Install dependencies

 pip install -r requirements.txt

 Features

- 🔐 Admin & Student login/register system
- 📄 Admin uploads academic PDFs
- 📚 PDFs are processed, chunked, and converted into embeddings
- 🧠 Embeddings stored in a vector database (e.g., FAISS)
- 💬 Students can enter queries in natural language
- 🤖 OpenAI API retrieves semantically relevant answers based on the content
- 📝 All questions and answers are stored in a database (via `db.py`)

# 🚀 Technologies Used

- Python
- OpenAI API
- Vector DB (FAISS)
- PDF Parser (`PyMuPDF`)
- Streamlit / Flask (depending on your UI)
- SQLite / PostgreSQL (for storing Q&A and user data)
- bcrypt / hashlib (for password hashing if applicable)

Admin Workflow:
1. Login via `login.py`
2. Upload PDFs via `chat.py`
3. PDFs are split, embedded, and stored in a vector database
4. Questions and responses are saved in `db.py` for records


Student Workflow:
1. Register/Login via `register.py` and `login.py`
2. Ask questions via `studentchat.py`
3. OpenAI retrieves matching chunks from the vector DB and returns an answer
4. Questions and responses are saved in `db.py` for records


RUNNING THE APPLICATION
python app.py
