import streamlit as st
import google.generativeai as genai
import PyPDF2
from io import BytesIO
import base64

# --- Configure Gemini API ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    st.session_state.ai_initialized = True
except Exception as e:
    st.error(f"Error configuring AI: {e}")
    st.session_state.ai_initialized = False

# --- Core AI Function ---
def get_ai_response(prompt_text, document_text):
    if not st.session_state.ai_initialized:
        return "AI model not available. Check API key."
    full_prompt = f"{prompt_text}\n\nDocument Text:\n{document_text}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error communicating with AI: {e}")
        return None

# --- PDF Text Extraction ---
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None
    return text

# --- Page Config ---
st.set_page_config(page_title="LexiGuide", page_icon="⚖", layout="wide")

# --- image bg ---
def get_base64_img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_img("assets/bg.png")  

# --- CSS & Background ---
st.markdown("""
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background: #412f26;
    color: #F5F5DC;
    font-family: 'Lora', serif;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Merriweather', serif;
    letter-spacing: 0.5px;
}
h1 { font-size: 3rem; color: #FFFFFF; font-weight: 700; }
h2 { color: #D2B48C; }
h3 { color: #F5F5DC; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1C1C1C !important;
    color: #F5F5DC !important;
    font-family: 'Lato', sans-serif;
}

/* Buttons */
.stButton>button {
    background-color: #5A3E2B !important; /* rich brown */
    color: #FFFFFF !important;
    font-weight: 600;
    border-radius: 6px;
    padding: 10px 20px;
    transition: all 0.3s ease;
    font-family: 'Lato', sans-serif;
}
.stButton>button:hover {
    background-color: #7B4F39 !important;
    box-shadow: 0 0 10px rgba(210,180,140,0.6);
}

/* Inputs */
textarea, input[type=text] {
    background-color: #2A2A2A !important;
    color: #F5F5DC !important;
    border-radius: 6px;
    font-family: 'Lato', sans-serif;
}

/* AI response cards */
.ai-card {
    background-color: #1F1F1F;
    color: #F5F5DC;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    font-family: 'Lato', sans-serif;
}

/* Info/Feature Boxes */
.info-box {
    background-color:#412f26 ;
    color: #F5F5DC;
    padding: 20px;
    border-radius: 12px;
    margin: 15px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    transition: transform 0.2s ease;
}
.info-box:hover { transform: translateY(-3px); }

/* Footer */
footer {
    font-size: 11px !important;
    color: #D2B48C !important;
    font-family: 'Lato', sans-serif;
}

/* Sleek Shapes */
.shape {
    position: absolute;
    border-radius: 50%;
    opacity: 0.06;
    background: #D6C0B3;
    animation: float 14s ease-in-out infinite;
}
.shape1 { width: 160px; height: 160px; top: 80px; left: 12%; }
.shape2 { width: 120px; height: 120px; top: 400px; left: 75%; }
.shape3 { width: 200px; height: 200px; top: 650px; left: 35%; }
.shape4 { width: 100px; height: 100px; top: 950px; left: 15%; }

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-25px); }
    100% { transform: translateY(0px); }
}
</style>

<div class="shape shape1"></div>
<div class="shape shape2"></div>
<div class="shape shape3"></div>
<div class="shape shape4"></div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown(f"""
<div style="
    text-align: center;
    padding: 2rem 0;
    max-width: 850px;
    margin:auto;
    background: linear-gradient(rgba(117, 82, 64, 0.9), rgba(117, 82, 64, 0.9)), 
                url('data:image/png;base64,{img_base64}') no-repeat center;
    background-size: cover;
    border-radius: 20px;
    color: #E4E0E1;
    border-bottom: 4px solid #D2B48C
">
    <h1>Clarity in Law. Confidence in Action.</h1>
    <h2 style='color:#F5F5DC;'>AI-Powered Legal Insights for Business Protection</h2>
    <p style="max-width:650px; margin:auto; color:#e5dfcc; font-size:1.1rem; line-height:1.6;">
        LexiGuide transforms complex contracts into clear guidance. From risk analysis to clause detection, 
        we simplify the law so you can focus on strategy.
    </p>
</div>
""", unsafe_allow_html=True)
# --- Example Info Boxes ---
st.markdown("""
<div style="display: flex; gap: 20px; justify-content: center; margin-top: 2rem;">
    <div class="info-box" style="flex:1; text-align:center;">
        <h3>📜 Contract Summaries</h3>
        <p>Plain-language summaries for instant clarity.</p>
    </div>
    <div class="info-box" style="flex:1; text-align:center;">
        <h3>🔑 Key Clauses</h3>
        <p>Spot crucial obligations, risks, and protections.</p>
    </div>
    <div class="info-box" style="flex:1; text-align:center;">
        <h3>💬 Legal Q&A</h3>
        <p>Ask questions and get AI-powered document answers.</p>
    </div>
</div>
""", unsafe_allow_html=True)



# --- Session State ---
if 'document_text' not in st.session_state:
    st.session_state.document_text = ""
if 'summary_analysis' not in st.session_state:
    st.session_state.summary_analysis = None
if 'clauses_analysis' not in st.session_state:
    st.session_state.clauses_analysis = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 📂 Upload Document")
    uploaded_file = st.file_uploader("", type="pdf")
    pasted_text = st.text_area("Or paste text here", height=150, placeholder="Paste your contract or agreement...")
    st.markdown("---")
    if st.button("⚡ Process Document", use_container_width=True):
        with st.spinner("Processing document..."):
            st.session_state.summary_analysis = None
            st.session_state.clauses_analysis = None
            if uploaded_file:
                st.session_state.document_text = extract_text_from_pdf(uploaded_file)
            elif pasted_text:
                st.session_state.document_text = pasted_text
            else:
                st.error("Please upload a PDF or paste text.")

# --- Main Area ---
if st.session_state.document_text and st.session_state.ai_initialized:
    st.success("✅ Document processed! Choose a tab below.")

    summary_tab, clauses_tab, qa_tab = st.tabs(
        ["📜 Summary & Risks", "🔑 Key Clauses", "💬 Ask Me Anything"]
    )

    with summary_tab:
        if not st.session_state.summary_analysis:
            with st.spinner("Generating summary & risk analysis..."):
                prompt = """
                Provide a two-part analysis:
                Part 1: Simple summary in plain English.
                Part 2: Traffic light clause analysis:
                  🔴 Red (Risks)
                  🟡 Yellow (Obligations)
                  🟢 Green (Favorable)
                """
                st.session_state.summary_analysis = get_ai_response(prompt, st.session_state.document_text)
        st.markdown(f"<div class='ai-card'>{st.session_state.summary_analysis}</div>", unsafe_allow_html=True)

    with clauses_tab:
        if not st.session_state.clauses_analysis:
            with st.spinner("Extracting key clauses..."):
                prompt = """
                Identify and explain key clauses:
                1. Clause title
                2. One-sentence explanation
                """
                st.session_state.clauses_analysis = get_ai_response(prompt, st.session_state.document_text)
        st.markdown(f"<div class='ai-card'>{st.session_state.clauses_analysis}</div>", unsafe_allow_html=True)

    with qa_tab:
        st.subheader("💬 Ask Questions About Your Document")
        user_question = st.chat_input("Type your question here...")
        if user_question:
            with st.spinner("Thinking..."):
                prompt = f"""
                Answer based ONLY on the document.
                If not found, say 'The document does not mention this.'
                User Question: {user_question}
                """
                answer = get_ai_response(prompt, st.session_state.document_text)
            if answer:
                with st.chat_message("assistant"):
                    st.markdown(f"<div class='ai-card'>{answer}</div>", unsafe_allow_html=True)

else:
    st.info("📥 Upload or paste a document on the left to get started.")

# --- Footer ---
st.markdown("<hr><p style='text-align:center; font-size:10px;'>⚖ LexiGuide | Built with Streamlit + Google Gemini API</p>", unsafe_allow_html=True)
