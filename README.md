
# ⚖️ Conversational Agentic AI Suite for Legal Document Drafting

This is a **multi-functional Legal AI Assistant** built using **Streamlit**, **LangChain**, and **Gemini Pro (via Google Generative AI)**. It enables users to:

- Interactively draft legal documents,
- Clarify legal queries in plain English,
- Perform document-based Q\&A using vector search.


## 🧠 Objective

To build a single, unified application with modular functionality that enables:

1. **Conversational Legal Document Drafting**
2. **Legal Clarification via API**
3. **Document-Based Question Answering**

This tool simulates an intelligent legal assistant with memory, comprehension, and information retrieval capabilities.

## 🧱 Technology Choices

| Component | Tool/Library Used | Reason |
| :-- | :-- | :-- |
| LLM | Gemini 1.5 Flash (via LangChain + Google Generative AI) | Powerful, free-tier model with multi-turn capabilities |
| Framework | Streamlit | Simple to prototype and deploy interactive apps |
| Vector Store | FAISS | Fast, local vector search (fully free, ideal for local use cases) |
| Embeddings | GoogleGenerativeAIEmbeddings | Matches LLM source (Gemini), ensuring compatible vector space |
| Memory | LangChain ConversationBufferMemory | Maintains user responses throughout drafting |
| PDF Parsing | PyPDFLoader | For loading legal documents |
| Document Splitter | RecursiveCharacterTextSplitter | Breaks documents into overlapping chunks for contextual QA |
| API Keys | python-dotenv | Securely manages environment secrets |

## 🏗️ Architecture Overview

```
User (Streamlit UI)
|
|--- Module 1: Legal Drafting (LLM + Memory)
|
|--- Module 2: Clarification (LLM only, API-ready)
|
|--- Module 3: Q&A on Uploaded Docs (LLM + FAISS + Embeddings)
|
Session Memory (Streamlit) → LLMs via LangChain → Gemini Models
```

Each module is **modular and independently testable**. The system runs as a unified application with a sidebar to switch between functionalities.

## 🧩 Module Breakdown

### 📄 Module 1: Conversational Document Drafter

- Initializes a conversational chain with memory
- Asks follow-up questions for missing legal inputs
- Remembers responses via session memory
- Returns a structured legal document draft


### 🧾 Module 2: Legal Clarification Tool

- Accepts any legal question from user
- Uses a zero-temperature Gemini LLM for factual responses
- (Extendable to external APIs like CanLII with URL-based queries)


### 📚 Module 3: Document Q\&A (Vector Search)

- Accepts PDF files (future: DOCX/TXT support)
- Extracts text, chunks it, generates embeddings
- Stores vectors in FAISS index
- Retrieves top-matching chunks using semantic similarity
- Answers user’s query using Gemini LLM over retrieved context


## 🚧 Implementation Strategy

### ✅ Modularization

Each module is in its own file under the `modules/` directory. They are imported and routed from `app.py` using a Streamlit dropdown selector.

### ✅ Prompt Engineering

- Drafting uses a custom multi-turn prompt with memory.
- Clarification uses a single-turn template prompt.
- Q\&A uses a context-injected prompt with vector retrieval.


### ✅ Deployment Constraints

- All APIs and services used are **free-tier**
- No paid model/API (as per task requirement)
- Ready for deployment on **Hugging Face Spaces**


## 📁 Project Structure

```
Agentic-AI-Suite-for-Legal-Tasks/
│
├── modules/
│   ├── module1_drafting.py      # Conversational Legal Drafting
│   ├── module2_clarification.py # Clarification using LLM
│   └── module3_qa.py            # Document Q&A via FAISS
│
├── app.py                         # Main Streamlit application
├── .env                           # API key for Google Gemini
├── requirements.txt               # All Python dependencies
└── README.md                      # You are reading it now 🙂
```


## ⚙️ Setup Instructions

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/para8ox-deb/Agentic-AI-Suite-for-Legal-Tasks.git
cd Agentic-AI-Suite-for-Legal-Tasks
```


### 🐍 2. Create \& Activate Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```


### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 🔐 4. Add Your API Key

Create a file named `.env` in the root directory:

```ini
GOOGLE_API_KEY=your_actual_google_api_key_here
```


### ▶️ 5. Run the App

```bash
streamlit run app.py
```


## 📈 Future Enhancements

- Add support for DOCX/TXT files in Document QA
- Use real legal APIs like CanLII in Module 2
- Download button for drafted documents
- Enhance UI with themes and icons


## 🔐 Disclaimer

This tool is not intended for real legal use. Outputs may contain inaccuracies. Always consult a licensed professional.

## 👤 Author

- **Developed by**: Aakash Kumar
- **Contact**: [LinkedIn](https://www.linkedin.com/in/para8ox-deb/)
- **GitHub**: [para8ox-deb](https://github.com/para8ox-deb)


## 📎 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

