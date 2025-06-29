from search import extract_keywords_from_jd

job_description = """
We're recruiting for a Software Engineer, ML Research role at Windsurf (the company behind Codeium) - a Forbes AI 50 company building AI-powered developer tools. They're looking for someone to train LLMs for code generation, with $140-300k + equity in Mountain View.
"""

keywords = extract_keywords_from_jd(job_description)
print("Extracted keywords:", keywords)

query = " ".join(keywords) + " site:linkedin.com/in/ Mountain View"
print("Final search query:", query) 