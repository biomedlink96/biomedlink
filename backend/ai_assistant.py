import httpx
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def ask_ai(query: str, manual_content: str) -> str:
    if not GROQ_API_KEY:
        return "AI service not available (missing API key)."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": f"You are a biomedical equipment assistant. Here is the equipment manual:\n{manual_content}"},
        {"role": "user", "content": query}
    ]

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json={
                "model": "llama3-8b-8192",
                "messages": messages,
                "temperature": 0.7
            })
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error contacting AI assistant: {str(e)}"
