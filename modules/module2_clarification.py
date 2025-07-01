import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


def setup_clarification_chain(api_key):
    """
    Sets up the legal clarification chain using the modern LCEL syntax.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.3)
    
    prompt_template = "You are a legal expert AI. Provide a clear explanation:\nQuestion: {question}\nAnswer:"
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

    chain = prompt | llm | StrOutputParser()
    
    return chain

def module2_ui(api_key):
    """
    Renders the Streamlit UI for the legal clarification tool.
    """
    st.header("⚖️ Legal Clarification Tool")

    if 'clarification_chain' not in st.session_state:
        st.session_state.clarification_chain = setup_clarification_chain(api_key)

    user_question = st.text_area("Enter your legal question:", height=150)

    if st.button("Get Clarification"):
        if user_question:
            with st.spinner("Fetching information..."):
                response = st.session_state.clarification_chain.invoke({"question": user_question})
                st.subheader("Answer:")
                st.info(response)
        else:
            st.warning("Please enter a question.")
