# app.py (Free Gemini API Version)

import streamlit as st
import google.generativeai as genai
import PyPDF2
from io import BytesIO

# --- Configure the Gemini API ---
try:
    # Get the API key from Streamlit's secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Load the Gemini 1.0 Pro model
    # New Code
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    st.session_state.ai_initialized = True
except Exception as e:
    st.error(f"Error configuring the AI model: {e}")
    st.error("Please make sure you have a GOOGLE_API_KEY in your .streamlit/secrets.toml file.")
    st.session_state.ai_initialized = False

# --- Core AI Function ---
def get_ai_response(prompt_text, document_text):
    """
    Sends a prompt and the document text to the Gemini model
    and returns the model's response.
    """
    if not st.session_state.ai_initialized:
        return "AI model is not available. Please check your API key configuration."

    # The complete prompt includes the instruction and the document context
    full_prompt = f"""
    {prompt_text}

    Here is the legal document text:
    ---
    {document_text}
    ---
    """
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        # Provide a more user-friendly error message
        st.error(f"An error occurred while communicating with the AI. Please check your API key and network connection. Details: {e}")
        return None


# --- Helper Function for PDF Text Extraction ---
def extract_text_from_pdf(pdf_file):
    """
    Extracts text from an uploaded PDF file.
    """
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None
    return text

# --- Streamlit UI (This is the NEW, updated section) ---

st.set_page_config(page_title="LexiGuide", page_icon="⚖️", layout="wide")

st.title("⚖️ LexiGuide: Demystify Your Legal Documents")
st.warning("Disclaimer: This is an AI-powered tool and not a substitute for professional legal advice. Always consult with a qualified attorney for legal matters.", icon="⚠️")

# Initialize session state for all variables
if 'document_text' not in st.session_state:
    st.session_state.document_text = ""
if 'summary_analysis' not in st.session_state:
    st.session_state.summary_analysis = None
if 'clauses_analysis' not in st.session_state:
    st.session_state.clauses_analysis = None


with st.sidebar:
    st.header("Upload Your Document")
    st.markdown("Upload a PDF or paste the text directly.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    pasted_text = st.text_area("Or paste text here", height=200)

    if st.button("Process Document", use_container_width=True):
        with st.spinner("Processing..."):
            # When a new document is processed, clear old results
            st.session_state.summary_analysis = None
            st.session_state.clauses_analysis = None
            
            if uploaded_file:
                st.session_state.document_text = extract_text_from_pdf(uploaded_file)
            elif pasted_text:
                st.session_state.document_text = pasted_text
            else:
                st.error("Please upload a file or paste text.")


if st.session_state.document_text and st.session_state.ai_initialized:
    st.success("Document processed! Select a tab below to see the analysis.")

    # Create tabs for different analyses
    summary_tab, clauses_tab, qa_tab = st.tabs(["📜 Summary & Risks", "🔑 Key Clauses", "💬 Ask a Question (Q&A)"])

    with summary_tab:
        # This analysis runs automatically if it hasn't been run before
        if not st.session_state.summary_analysis:
            with st.spinner("Generating summary and risk analysis..."):
                prompt = """
                You are an expert legal analyst. Your task is to provide a two-part analysis of the legal document below.

                **Part 1: Simple Summary**
                First, write a concise, plain-English summary of the document. Explain its main purpose and what it means for the person signing it.

                **Part 2: Traffic Light Clause Analysis**
                After the summary, categorize the key clauses into a "Traffic Light" system. For each clause, provide a title and a simple one-sentence explanation.

                ---

                ### 🔴 Red Light Clauses (Risks & Dangers)
                List all clauses that represent significant risks, penalties, liabilities, restrictions, or unfavorable terms. These are critical "must-know" items.

                ### 🟡 Yellow Light Clauses (Caution & Obligations)
                List all clauses that require specific attention, outline the user's duties and obligations, or detail important procedures like renewals or termination notices.

                ### 🟢 Green Light Clauses (Favorable & Standard)
                List all clauses that are standard, benign, or that outline the user's rights and the services they will receive.
                """
                st.session_state.summary_analysis = get_ai_response(prompt, st.session_state.document_text)

        # Always display the result from session state
        st.markdown(st.session_state.summary_analysis)

    with clauses_tab:
        # This analysis runs automatically as well
        if not st.session_state.clauses_analysis:
            with st.spinner("Extracting key clauses..."):
                prompt = """
                You are an expert legal analyst. Your task is to identify and explain the key clauses
                in the provided legal document. For each key clause, provide:
                1. The Clause Title (e.g., "Term of Agreement", "Confidentiality", "Termination").
                2. A simple, one-sentence explanation of what the clause means for the user.
                Format the output clearly with headings for each clause.
                """
                st.session_state.clauses_analysis = get_ai_response(prompt, st.session_state.document_text)

        # Always display the result from session state
        st.markdown(st.session_state.clauses_analysis)

    with qa_tab:
        # The Q&A tab remains interactive, so it still needs a button
        st.subheader("Ask Questions About Your Document")
        user_question = st.text_input("Enter your question here:")
        if st.button("Get Answer", key="qa_btn"):
            if user_question:
                prompt = f'''
                You are a legal Q&A assistant. You must answer the user's question based *only* on the
                information available in the provided legal document. Do not make assumptions or use
                external knowledge. If the answer is not in the document, state that clearly.

                User's Question: "{user_question}"
                '''
                with st.spinner("Finding answer..."):
                    answer = get_ai_response(prompt, st.session_state.document_text)
                    if answer:
                        st.markdown(answer)
            else:
                st.warning("Please enter a question.")
else:
    st.info("Upload or paste a document on the left to get started.")