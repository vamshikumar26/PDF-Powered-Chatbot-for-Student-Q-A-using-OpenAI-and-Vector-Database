import streamlit as st
import os
import faiss
import pickle
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
BASE_DIR = "uploaded_pdfs"

def process_pdf(file_path):
    doc_reader = PdfReader(file_path)
    raw_text = ''
    for i, page in enumerate(doc_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    return docsearch

def save_uploaded_file(uploaded_file, year, semester):
    dir_path = os.path.join(BASE_DIR, year, semester)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def save_faiss_index(docsearch, year, semester, file_name):
    index_path = os.path.join(BASE_DIR, year, semester, f"{file_name}_index.faiss")
    faiss.write_index(docsearch.index, index_path)
    with open(os.path.join(BASE_DIR, year, semester, f"{file_name}_docstore.pkl"), "wb") as f:
        pickle.dump(docsearch.docstore._dict, f)  # Directly save the internal dictionary
    with open(os.path.join(BASE_DIR, year, semester, f"{file_name}_index_to_docstore_id.pkl"), "wb") as f:
        pickle.dump(docsearch.index_to_docstore_id, f)

def load_faiss_index(year, semester, file_name, embeddings):
    index_path = os.path.join(BASE_DIR, year, semester, f"{file_name}_index.faiss")
    docstore_path = os.path.join(BASE_DIR, year, semester, f"{file_name}_docstore.pkl")
    index_to_docstore_id_path = os.path.join(BASE_DIR, year, semester, f"{file_name}_index_to_docstore_id.pkl")
    
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

def upload_page():
    st.title("Upload PDF")

    year = st.selectbox("Select Year", ["Year 1", "Year 2", "Year 3", "Year 4"])
    
    if year:
        semester = st.selectbox("Select Semester", ["Semester 1", "Semester 2"])
    
    if year and semester:
        uploaded_files = st.file_uploader(f"Upload PDFs for {year} - {semester}", type="pdf", accept_multiple_files=True)
        
        if uploaded_files:
            embeddings = OpenAIEmbeddings()
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file, year, semester)
                docsearch = process_pdf(file_path)
                save_faiss_index(docsearch, year, semester, uploaded_file.name)
                st.success(f"PDF '{uploaded_file.name}' uploaded and processed for {year} - {semester} successfully!")

    st.subheader("Uploaded Files")
    if os.path.exists(BASE_DIR):
        for year_dir in os.listdir(BASE_DIR):
            year_path = os.path.join(BASE_DIR, year_dir)
            if os.path.isdir(year_path):
                for semester_dir in os.listdir(year_path):
                    semester_path = os.path.join(year_path, semester_dir)
                    if os.path.isdir(semester_path):
                        st.write(f"**{year_dir} - {semester_dir}:**")
                        for file_name in os.listdir(semester_path):
                            if file_name.endswith(".pdf"):
                                st.write(f"- {file_name}")
    else:
        st.write("No files uploaded yet.")

def chatbot_page():
    st.title("Chatbot")

    if any(key for key in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, key))):
        year = st.selectbox("Select Year for Query", ["Year 1", "Year 2", "Year 3", "Year 4"])
        if year:
            semester = st.selectbox("Select Semester for Query", ["Semester 1", "Semester 2"])

        if year and semester:
            try:
                files_path = os.path.join(BASE_DIR, year, semester)
                files = [f for f in os.listdir(files_path) if f.endswith(".pdf")]
                
                if files:
                    file_name = st.selectbox("Select a file", files)
                    query = st.text_input("Enter your query")
                    if query:
                        embeddings = OpenAIEmbeddings()
                        docsearch = load_faiss_index(year, semester, file_name, embeddings)
                        if docsearch:
                            retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
                            rqa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
                            result = rqa(query)['result']
                            st.write(f"Answer", result)
                        else:
                            st.warning(f"No embeddings found for '{file_name}'. Please re-upload the PDF.")
                else:
                    st.warning("No PDF files found in the selected year and semester.")
            except FileNotFoundError:
                st.warning("There are no files available for the selected year and semester.")
    else:
        st.warning("Please upload a PDF file first.")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload PDF", "Chatbot"])

if page == "Upload PDF":
    upload_page()
else:
    chatbot_page()
