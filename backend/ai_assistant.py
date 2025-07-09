import os
import httpx

# Load API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Async function to call Groq's LLaMA 3 model
async def ask_ai(query: str) -> str:
    if not GROQ_API_KEY:
        return "Error: GROQ API key not found."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a biomedical equipment assistant. "
                    "Answer questions clearly and accurately, based on medical equipment manuals "
                    "and WHO/iHTM standards."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"AI Error: {str(e)}"
