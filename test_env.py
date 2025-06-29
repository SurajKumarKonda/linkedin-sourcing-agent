import os
from dotenv import load_dotenv

print("Before load_dotenv():")
print("SERPAPI_KEY:", os.getenv('SERPAPI_KEY'))
print("RAPIDAPI_KEY:", os.getenv('RAPIDAPI_KEY'))

print("\nLoading .env file...")
load_dotenv()

print("\nAfter load_dotenv():")
print("SERPAPI_KEY:", os.getenv('SERPAPI_KEY')[:10] + "..." if os.getenv('SERPAPI_KEY') else "Not found")
print("RAPIDAPI_KEY:", os.getenv('RAPIDAPI_KEY')[:10] + "..." if os.getenv('RAPIDAPI_KEY') else "Not found")

# Test the search function directly
print("\nTesting search function...")
from search import search_candidates

try:
    candidates = search_candidates("machine learning engineer", location="Mountain View", num_results=5)
    print(f"Found {len(candidates)} candidates")
    for i, candidate in enumerate(candidates):
        print(f"{i+1}. {candidate['name']} - {candidate['linkedin_url']}")
except Exception as e:
    print(f"Error in search: {e}") 