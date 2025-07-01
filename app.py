import streamlit as st
import os
from dotenv import load_dotenv
from modules.module1_drafting import module1_ui
from modules.module2_clarification import module2_ui
from modules.module3_qa import module3_ui

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found.")
    st.stop()

st.set_page_config(page_title="Legal AI Suite", layout="wide")
st.title("Conversational Agentic AI Suite for Legal Tasks")

st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a module", [
    "Legal Document Drafting", "Legal Clarification", "Document Q&A"
])

# Route modules
if app_mode == "Legal Document Drafting":
    if st.sidebar.button("Clear Drafting Chat", key="clear_drafting"):
        if "drafting_history" in st.session_state:
            st.session_state.drafting_history = []
        if "drafting_conversation" in st.session_state:
            del st.session_state.drafting_conversation
        st.rerun()
    module1_ui(api_key)

elif app_mode == "Legal Clarification":
    module2_ui(api_key)

elif app_mode == "Document Q&A":
    module3_ui(api_key)
