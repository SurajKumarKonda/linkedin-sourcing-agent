import os
from dotenv import load_dotenv
from search import search_candidates

load_dotenv()

# Test with simpler queries
test_queries = [
    "machine learning engineer",
    "software engineer",
    "AI engineer",
    "ML engineer"
]

for query in test_queries:
    print(f"\n🔍 Testing query: '{query}'")
    candidates = search_candidates(query, location="Mountain View", num_results=5)
    print(f"Found {len(candidates)} candidates")
    
    if candidates:
        for i, candidate in enumerate(candidates, 1):
            print(f"  {i}. {candidate['name']} - {candidate['linkedin_url']}")
    else:
        print("  No candidates found") 