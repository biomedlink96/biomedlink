import httpx
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def ask_ai(query: str) -> str:
    if not GROQ_API_KEY:
        return "AI service not available (missing API key)."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a biomedical equipment assistant."},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error contacting AI assistant: {str(e)}"
