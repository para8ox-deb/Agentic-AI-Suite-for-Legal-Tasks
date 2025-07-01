import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

def setup_qa_chain(api_key):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    prompt_template = PromptTemplate(
        template="""Answer the question based only on the provided context.
If the answer is not in the context, say so.

Context:
{context}

Question:
{question}

Answer:""",
        input_variables=["context", "question"]
    )
    chain = (
        RunnableMap({
            "context": lambda x: "\n\n".join(doc.page_content for doc in x["input_documents"]),
            "question": lambda x: x["question"]
        })
        | prompt_template | llm | StrOutputParser()
    )
    return chain

def process_pdf_for_qa(file, api_key):
    with open(file.name, "wb") as f:
        f.write(file.getbuffer())
    loader = PyPDFLoader(file.name)
    pages = loader.load_and_split()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_documents(pages)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_documents(texts, embeddings)
    os.remove(file.name)
    return vector_store

def module3_ui(api_key):
    st.header("Document-Based Q&A")
    qa_chain = setup_qa_chain(api_key)
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="qa_uploader")

    if uploaded_file:
        if 'qa_vector_store' not in st.session_state or st.session_state.get('qa_file_name') != uploaded_file.name:
            with st.spinner("Processing document..."):
                st.session_state.qa_vector_store = process_pdf_for_qa(uploaded_file, api_key)
                st.session_state.qa_file_name = uploaded_file.name
                st.success("Document processed.")

    if 'qa_vector_store' in st.session_state:
        user_question = st.text_input("Ask a question:")
        if st.button("Get Answer"):
            if user_question:
                with st.spinner("Searching..."):
                    docs = st.session_state.qa_vector_store.similarity_search(user_question)
                    response = qa_chain.invoke({"input_documents": docs, "question": user_question})
                    st.subheader("Answer:")
                    st.write(response)
            else:
                st.warning("Please enter a question.")
