import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")  # set in .env or your terminal

COMMON_AI_KEYWORDS = [
    "LLM", "LangChain", "RAG", "code generation", "AI engineer", "NLP", "transformer",
    "deep learning", "ML", "foundation model", "machine learning", "software engineer"
]

def extract_keywords_from_jd(jd_text):
    jd_lower = jd_text.lower()
    return [kw for kw in COMMON_AI_KEYWORDS if kw.lower() in jd_lower]

def search_candidates(job_description_text, location=None, num_results=10):
    keywords = extract_keywords_from_jd(job_description_text)
    if not keywords:
        keywords = ["AI engineer"]  # fallback

    query = " ".join(keywords) + " site:linkedin.com/in/"
    if location:
        query += f" {location}"

    print(f"Using search query: {query}")

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()

    candidates = []
    for result in results.get("organic_results", []):
        link = result.get("link", "")
        if "linkedin.com/in/" in link:
            candidates.append({
                "name": result.get("title", ""),
                "linkedin_url": link,
                "position": result.get("snippet", "")
            })

    return candidates