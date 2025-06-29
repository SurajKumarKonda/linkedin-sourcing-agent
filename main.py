from search import search_candidates
from score import score_candidates
from outreach import generate_messages
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_job_description_from_user():
    """Get job description from user input"""
    print("🎯 LinkedIn Sourcing Agent")
    print("=" * 50)
    print("Enter the job description below. Press Enter twice when finished:")
    print("(You can paste a multi-line job description)")
    print("-" * 50)
    
    lines = []
    while True:
        line = input()
        if line.strip() == "" and lines:  # Empty line and we have content
            break
        lines.append(line)
    
    job_description = "\n".join(lines).strip()
    
    if not job_description:
        print("❌ No job description provided. Using default...")
        job_description = """
We're recruiting for a Software Engineer, ML Research role at Windsurf (the company behind Codeium) - a Forbes AI 50 company building AI-powered developer tools. They're looking for someone to train LLMs for code generation, with $140-300k + equity in Mountain View.
"""
    
    return job_description

def get_search_parameters():
    """Get additional search parameters from user"""
    print("\n🔍 Search Parameters")
    print("-" * 30)
    
    # Location
    location = input("Location (default: Mountain View): ").strip()
    if not location:
        location = "Mountain View"
    
    # Number of candidates
    while True:
        num_candidates_input = input("Number of candidates to find (default: 10): ").strip()
        if not num_candidates_input:
            num_candidates = 10
            break
        try:
            num_candidates = int(num_candidates_input)
            if num_candidates > 0 and num_candidates <= 50:
                break
            else:
                print("Please enter a number between 1 and 50.")
        except ValueError:
            print("Please enter a valid number.")
    
    return location, num_candidates

def main():
    try:
        # Get job description from user
        job_description = get_job_description_from_user()
        
        # Get search parameters
        location, num_candidates = get_search_parameters()
        
        print(f"\n📋 Job Description:")
        print("-" * 30)
        print(job_description)
        print(f"\n📍 Location: {location}")
        print(f"👥 Target Candidates: {num_candidates}")
        print("\n" + "=" * 50)
        
        # Step 1: Search candidates
        print("🔍 Searching for candidates...")
        candidates = search_candidates(job_description, location=location, num_results=num_candidates)
        print(f"Found {len(candidates)} candidates")

        if not candidates:
            print("No candidates found. Exiting.")
            return

        # Step 2: Score candidates
        print("📊 Scoring candidates...")
        scored = score_candidates(candidates, job_description)
        print(f"Successfully scored {len(scored)} candidates")

        if not scored:
            print("No candidates could be scored. Exiting.")
            return

        # Step 3: Generate outreach
        print("✉️ Generating outreach messages...")
        messages = generate_messages(scored[:num_candidates], job_description)

        # Step 4: Format output as JSON
        output = {
            "job_id": f"job-{hash(job_description) % 1000000}",
            "candidates_found": len(candidates),
            "top_candidates": []
        }

        # Create message lookup for easy access
        message_lookup = {msg["candidate"]: msg["message"] for msg in messages}

        # Build top candidates list
        for candidate in scored[:num_candidates]:  # Top candidates
            candidate_output = {
                "name": candidate["candidate"],
                "linkedin_url": candidate["linkedin_url"],
                "fit_score": candidate["score"],
                "score_breakdown": candidate["scores"],
                "outreach_message": message_lookup.get(candidate["candidate"], "Message not generated")
            }
            output["top_candidates"].append(candidate_output)

        # Print formatted JSON output
        print("\n" + "=" * 50)
        print("🎯 RECRUITMENT RESULTS")
        print("=" * 50)
        print(json.dumps(output, indent=2))

        # Also save to file
        filename = f"recruitment_results_{output['job_id']}.json"
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n💾 Results saved to {filename}")

    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure you have set the required environment variables:")
        print("- SERPAPI_API_KEY")
        print("- RAPIDAPI_KEY")

if __name__ == "__main__":
    main()