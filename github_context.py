# github_context.py
import requests
from config import GITHUB_TOKEN, REPO

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_issues():
    url = f"https://api.github.com/repos/{REPO}/issues"
    resp = requests.get(url, headers=HEADERS)
    return [i["title"] + "\n" + i["body"] for i in resp.json() if "pull_request" not in i]

def fetch_readme():
    url = f"https://api.github.com/repos/{REPO}/readme"
    resp = requests.get(url, headers=HEADERS)
    content = requests.get(resp.json()["download_url"]).text
    return content
