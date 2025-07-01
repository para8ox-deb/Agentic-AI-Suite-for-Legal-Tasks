import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain

def setup_drafting_agent(api_key):
    """
    Sets up the conversational drafting agent using modern LangChain components.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a conversational AI assistant specializing in legal document drafting. Your goal is to help a user draft a legal document.

Instructions:
1. Start by asking the user what type of legal document they want to draft.
2. Identify key information needed and ask for it conversationally.
3. Use the conversation history to remember answers.
4. When ready, generate a complete, well-structured document.
"""
            ),
            MessagesPlaceholder(variable_name="history"), # Placeholder for chat history
            ("human", "{input}"),
        ]
    )

    return prompt | llm

def module1_ui(api_key):
    """
    Renders the Streamlit UI for the conversational drafter.
    """
    st.header("📜 Conversational Legal Document Drafter")

    # Initialize session state for history if it doesn't exist
    if 'drafting_history' not in st.session_state:
        st.session_state.drafting_history = []

    # Initialize the conversational chain
    if 'drafting_chain' not in st.session_state:
        st.session_state.drafting_chain = setup_drafting_agent(api_key)

    # Display prior chat messages from history
    for message in st.session_state.drafting_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

    # Get user input
    user_input = st.chat_input("Start drafting your document...")
    if user_input:
        # Append user message to history and display it
        st.session_state.drafting_history.append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        with st.spinner("Thinking..."):
            # Invoke the chain with the current history and new input
            response = st.session_state.drafting_chain.invoke(
                {"history": st.session_state.drafting_history, "input": user_input}
            )

        # Append AI response to history and display it
        st.session_state.drafting_history.append(AIMessage(content=response.content))
        with st.chat_message("assistant"):
            st.markdown(response.content)

