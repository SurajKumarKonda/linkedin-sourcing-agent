import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
print(f"API Key loaded: {bool(SERPAPI_API_KEY)}")

# Test a simple Google search first
params = {
    "engine": "google",
    "q": "machine learning engineer",
    "api_key": SERPAPI_API_KEY,
    "num": 3
}

print("Testing basic Google search...")
response = requests.get("https://serpapi.com/search", params=params)
results = response.json()

print(f"Status: {response.status_code}")
print(f"Results found: {len(results.get('organic_results', []))}")

if results.get('organic_results'):
    for i, result in enumerate(results['organic_results'][:3], 1):
        print(f"{i}. {result.get('title', 'No title')} - {result.get('link', 'No link')}")

# Test LinkedIn specific search
print("\nTesting LinkedIn search...")
params["q"] = "machine learning engineer site:linkedin.com/in/"

response = requests.get("https://serpapi.com/search", params=params)
results = response.json()

print(f"Status: {response.status_code}")
print(f"Results found: {len(results.get('organic_results', []))}")

if results.get('organic_results'):
    for i, result in enumerate(results['organic_results'][:3], 1):
        print(f"{i}. {result.get('title', 'No title')} - {result.get('link', 'No link')}")
else:
    print("No LinkedIn results found") 