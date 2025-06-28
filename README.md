# 🤖 PDF-Powered Chatbot for Student Q&A using OpenAI and Vector Database

This project is an AI-based chatbot system designed to help students get answers from academic documents (PDFs) uploaded by an admin. The PDFs are converted into embeddings and stored in a vector database, allowing the chatbot to retrieve contextually relevant information when students ask queries. The chatbot uses OpenAI’s language model to generate answers based on these embeddings.

---

## 🧠 Key Features

- Admin can upload one or more academic PDFs
- PDF content is chunked and converted into embeddings
- Embeddings are stored in a vector database (e.g., FAISS, Chroma, Pinecone, etc.)
- Students can ask natural language queries
- OpenAI API retrieves the most relevant chunks and generates an answer

---

## 🗂️ Project Structure



 Install dependencies

 pip install -r requirements.txt
