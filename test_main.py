import os
from dotenv import load_dotenv
from search import search_candidates

load_dotenv()

job_description = """
We're recruiting for a Software Engineer, ML Research role at Windsurf (the company behind Codeium) - a Forbes AI 50 company building AI-powered developer tools. They're looking for someone to train LLMs for code generation, with $140-300k + equity in Mountain View.
"""

print("🔍 Searching for candidates...")
print(f"Job description: {job_description[:100]}...")

candidates = search_candidates(job_description, location="Mountain View", num_results=10)
print(f"Found {len(candidates)} candidates")

if candidates:
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate['name']} - {candidate['linkedin_url']}")
else:
    print("No candidates found.") 