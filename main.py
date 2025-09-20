# main.py (This is your new backend)
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# --- Configuration ---
# It's better to use environment variables for API keys
# For now, you can keep using st.secrets or os.getenv
# Make sure you have your GOOGLE_API_KEY set up
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the FastAPI app
app = FastAPI()

# Define the data model for incoming requests
class DocumentRequest(BaseModel):
    document_text: str
    prompt_type: str # e.g., "summary" or "clauses"

# The core AI function (no changes needed here)
def get_ai_response(prompt, document_text):
    model = genai.GenerativeModel("gemini-1.0-pro") # Or 1.5-flash
    full_prompt = f"{prompt}\n\nHere is the document:\n---\n{document_text}"
    response = model.generate_content(full_prompt)
    return response.text

# --- API Endpoint ---
@app.post("/analyze")
def analyze_document(request: DocumentRequest):
    # Define your prompts here
    prompts = {
        "summary": """
        You are an expert legal analyst... (Your full summary prompt here)
        """,
        "clauses": """
        You are an expert legal analyst... (Your full clauses prompt here)
        """
    }

    prompt_to_use = prompts.get(request.prompt_type)
    if not prompt_to_use:
        return {"error": "Invalid prompt type"}

    # Call the AI function and return the result
    analysis_result = get_ai_response(prompt_to_use, request.document_text)
    return {"analysis": analysis_result}