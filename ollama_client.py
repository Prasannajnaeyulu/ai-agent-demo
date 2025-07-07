import httpx

OLLAMA_URL = "http://ollama:11434/api/generate"

async def ask_ollama(prompt: str, model="llama3"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json=payload)
        return response.json()["response"]
