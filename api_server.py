from fastapi import FastAPI, Header, HTTPException
import requests
import os

app = FastAPI()

# Security token fetched from Render environment variables
API_SECRET = os.environ.get("BUZZBOT_SECRET", "Buzzbot-Milon-2026-ChangeMe")

# Groq API key fetched securely from Render environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.get("/")
def home():
    return {"status": "Buzzbot API is running successfully"}

@app.post("/chat")
def chat(data: dict, x_buzzbot_key: str = Header(default="")):
    # 1. Security Authorization Check
    if x_buzzbot_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    question = data.get("question", "").strip()
    if not question:
        return {"answer": "Please ask a question."}

    # 2. Forward the request to Groq Cloud infrastructure
    try:
        url = "https://groq.com"  # Corrected API Endpoint
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",  
            "messages": [{"role": "user", "content": question}]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        # Extract text response safely
        ai_response = result["choices"][0]["message"]["content"]
        return {"answer": ai_response}
        
    except Exception as e:
        # If response exists, return its raw error text to debug
        if 'response' in locals() and hasattr(response, 'text'):
            return {"answer": f"Groq Error Detail: {response.text}"}
        return {"answer": f"Cloud AI Service Error: {str(e)}"}
