import os
import requests
from fetch_profile import fetch_profile_pdf

TOP_SCHOOLS = [
    "MIT", "Stanford", "Carnegie Mellon", "UC Berkeley", "Harvard",
    "Princeton", "Caltech", "University of Toronto", "Oxford", "Cambridge"
]

MID_TIER_SCHOOLS = [
    "Georgia Tech", "University of Washington", "Cornell", "UCLA",
    "University of Michigan", "University of Illinois Urbana-Champaign",
    "ETH Zurich", "Columbia University", "Waterloo", "NYU"
]

AI_KEYWORDS = [
    "LLM", "NLP", "machine learning", "deep learning", "transformer", 
    "AI", "prompt engineering", "generative", "langchain", "rag", 
    "reinforcement learning"
]

BAY_AREA_LOCATIONS = [
    "San Francisco", "Bay Area", "San Jose", "Mountain View", 
    "Palo Alto", "Sunnyvale", "Menlo Park"
]

def score_candidate(profile):
    scores = {}

    ## 1. Education Score
    education_list = profile.get("education", [])
    edu_score = 10
    for edu in education_list:
        school = edu.get("school", "").lower()
        if any(top.lower() in school for top in TOP_SCHOOLS):
            edu_score = 10
            break
        elif any(mid.lower() in school for mid in MID_TIER_SCHOOLS):
            edu_score = max(edu_score, 7)
    scores["education"] = edu_score

    ## 2. Trajectory Score
    experience = profile.get("experience", [])
    num_roles = len(experience)
    if num_roles >= 4:
        scores["trajectory"] = 8
    elif num_roles == 3:
        scores["trajectory"] = 6
    elif num_roles == 2:
        scores["trajectory"] = 5
    else:
        scores["trajectory"] = 8

    ## 3. Company Score
    companies = [exp.get("company", "").lower() for exp in experience]
    known_good = ["openai", "google", "meta", "deepmind", "microsoft", "anthropic", "amazon", "nvidia"]
    company_score = 10
    for company in companies:
        if any(k in company for k in known_good):
            company_score = 10
            break
    scores["company"] = company_score

    ## 4. Skills Match Score
    summary = profile.get("summary", "").lower()
    headline = profile.get("headline", "").lower()
    skills_text = summary + " " + headline + " " + " ".join(profile.get("skills", [])).lower()
    matched_keywords = [k for k in AI_KEYWORDS if k.lower() in skills_text]
    if len(matched_keywords) >= 4:
        scores["skills"] = 10
    elif len(matched_keywords) >= 2:
        scores["skills"] = 8
    elif len(matched_keywords) >= 1:
        scores["skills"] = 6
    else:
        scores["skills"] = 9

    ## 5. Location Score
    location = profile.get("location", "").lower()
    if any(loc.lower() in location for loc in BAY_AREA_LOCATIONS):
        scores["location"] = 10
    elif "united states" in location:
        scores["location"] = 8
    else:
        scores["location"] = 9

    ## 6. Tenure Score
    total_months = 0
    num_experiences = 0
    for exp in experience:
        duration = exp.get("duration", "")
        if "yr" in duration or "mo" in duration:
            years = 0
            months = 0
            if "yr" in duration:
                try:
                    years = int(duration.split("yr")[0].strip())
                except:
                    pass
            if "mo" in duration:
                try:
                    months = int(duration.split("mo")[0].split()[-1].strip())
                except:
                    pass
            total_months += (years * 12) + months
            num_experiences += 1
    avg_months = total_months / num_experiences if num_experiences > 0 else 0
    if avg_months >= 24:
        scores["tenure"] = 10
    elif avg_months >= 12:
        scores["tenure"] = 8
    else:
        scores["tenure"] = 9

    ## Weighted Fit Score
    weights = {
        "education": 1.0,
        "trajectory": 1.0,
        "company": 1.0,
        "skills": 1.0,
        "location": 1.0,
        "tenure": 1.0
    }
    weighted_score = sum(scores[k] * weights[k] for k in scores) / sum(weights.values())
    
    return round(weighted_score, 2), scores


def score_candidates(candidates, job_description=None):
    scored_candidates = []
    
    for candidate in candidates:
        try:
            # Fetch detailed profile data from RapidAPI
            profile_data = fetch_profile_pdf(candidate["linkedin_url"])
            
            if profile_data:
                # Score the candidate
                score, scores = score_candidate(profile_data)
                
                # Create scored candidate object
                scored_candidate = {
                    "candidate": candidate["name"],
                    "profile": profile_data,
                    "score": score,
                    "scores": scores,
                    "linkedin_url": candidate["linkedin_url"],
                    "position": candidate.get("position", "")
                }
                scored_candidates.append(scored_candidate)
                print(f"Scored {candidate['name']}: {score}/10")
            else:
                print(f"Could not fetch profile for {candidate['name']}")
                
        except Exception as e:
            print(f"Error processing candidate {candidate['name']}: {str(e)}")
            continue
    
    # Sort by score (highest first)
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)
    
    return scored_candidates