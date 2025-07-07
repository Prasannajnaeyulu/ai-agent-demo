import os
import httpx
import requests
from fastapi import APIRouter, Request
from dotenv import load_dotenv
import base64

load_dotenv()

router = APIRouter()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_BOT_ID = os.getenv("SLACK_BOT_ID")  # Required to strip mentions like <@U12345>
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
GITHUB_REPO = os.getenv("GITHUB_REPO", "microsoft/semantic-kernel")  # format: owner/repo

@router.post("/slack/events")
async def slack_events(request: Request):
    body = await request.json()

    # Slack URL verification challenge
    if body.get("type") == "url_verification":
        return {"challenge": body["challenge"]}

    event = body.get("event", {})
    if event.get("type") == "app_mention":
        text = event.get("text", "")
        channel = event.get("channel")

        # Strip the bot mention (e.g., <@U12345>) from the message
        clean_text = text.replace(f"<@{SLACK_BOT_ID}>", "").strip()

        # 1. Get GitHub context (issues + README)
        context = await get_github_context("microsoft", "semantic-kernel")

        # 2. Create prompt
        prompt = (
            f"You are an assistant. A user asked the following question:\n"
            f"\"{clean_text}\"\n\n"
            f"Use the following GitHub context to help answer:\n\n{context}"
        )

        # 3. Ask Ollama
        response = await query_ollama(prompt)

        # 4. Send reply to Slack
        await post_to_slack(channel, response)

    return {"ok": True}

# ========== GitHub ==========
async def get_github_context(owner: str, repo: str, limit=3) -> str:
    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    async with httpx.AsyncClient() as client:
        # --- Fetch issues ---
        issues = []
        try:
            resp = await client.get(issues_url, headers=headers)
            if resp.status_code == 200:
                issues_data = resp.json()
                issues = [
                    f"Issue: {i['title']}\n{i.get('body', '')[:200]}"
                    for i in issues_data[:limit]
                ]
        except Exception:
            issues.append("Could not load issues.")

        # --- Fetch README content ---
        readme_text = ""
        try:
            resp = await client.get(readme_url, headers=headers)
            if resp.status_code == 200:
                readme_data = resp.json()
                readme_text = base64.b64decode(readme_data["content"]).decode("utf-8")[:1500]
        except Exception:
            readme_text = "Could not load README."

        # --- Combine context ---
        combined = "\n\n".join(issues) + "\n\n--- README ---\n\n" + readme_text
        return combined

# ========== Ollama ==========
async def query_ollama(prompt: str) -> str:
    print(f"Querying Ollama with prompt: {prompt[:80]}...")
    timeout = httpx.Timeout(connect=10.0, read=300.0, write=30.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": "gemma3:1b", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

# ========== Slack ==========
async def post_to_slack(channel: str, message: str):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"channel": channel, "text": message}
    async with httpx.AsyncClient() as client:
        await client.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
