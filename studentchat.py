import os
import pickle
import faiss
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def load_faiss_index(year, semester, subject_name, embeddings):
    BASE_DIR = "uploaded_pdfs"
    index_path = os.path.join(BASE_DIR, year, semester, subject_name, f"{subject_name}_index.faiss")
    docstore_path = os.path.join(BASE_DIR, year, semester, subject_name, f"{subject_name}_docstore.pkl")
    index_to_docstore_id_path = os.path.join(BASE_DIR, year, semester, subject_name, f"{subject_name}_index_to_docstore_id.pkl")
    
    if os.path.exists(index_path) and os.path.exists(docstore_path) and os.path.exists(index_to_docstore_id_path):
        index = faiss.read_index(index_path)
        with open(docstore_path, "rb") as f:
            docstore_dict = pickle.load(f)
        docstore = InMemoryDocstore(docstore_dict)
        with open(index_to_docstore_id_path, "rb") as f:
            index_to_docstore_id = pickle.load(f)
        docsearch = FAISS(embeddings.embed_query, index, docstore, index_to_docstore_id)
        return docsearch
    return None

def chatbot_page(switch_page):
    st.title("Chatbot")

    BASE_DIR = "uploaded_pdfs"
    if any(key for key in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, key))):
        year = st.selectbox("Select Year for Query", ["Year 1", "Year 2", "Year 3", "Year 4"])
        if year:
            semester = st.selectbox("Select Semester for Query", ["Semester 1", "Semester 2"])
        if year and semester:
            subject_name = st.selectbox("Select Subject", ["machine learning", "deep learning"])
            mark_type = st.selectbox("Select Mark Type", ["2 marks", "7 marks", "14 marks"])

        if year and semester and subject_name and mark_type:
            try:
                query = st.text_input("Enter your query")
                if query:
                    query = f"{query} (Mark Type: {mark_type})"
                    print(query)
                if query:
                    load_dotenv()
                    embeddings = OpenAIEmbeddings()
                    docsearch = load_faiss_index(year, semester, subject_name, embeddings)
                    if docsearch:
                        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
                        rqa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
                        result = rqa(query)['result']
                        st.write(f"**Answer**: {result}")
                        
                    else:
                        st.warning(f"No embeddings found for  subject {subject_name}. Please re-upload the PDF.")
            except FileNotFoundError:
                st.warning("There are no files available for the selected year, semester, and subject.")
            
        else:
            st.warning("Please select year, semester, and subject first.")
