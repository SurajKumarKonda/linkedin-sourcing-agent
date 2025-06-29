# This file is for Hugging Face Spaces deployment
# It's the same as api.py but with the correct structure for Spaces

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from search import search_candidates
from score import score_candidates
from outreach import generate_messages
import json

# Load environment variables
load_dotenv()

app = FastAPI(
    title="LinkedIn Sourcing Agent API",
    description="AI-powered LinkedIn candidate sourcing and outreach generation",
    version="1.0.0"
)

class JobRequest(BaseModel):
    job_description: str
    location: Optional[str] = "Mountain View"
    num_candidates: Optional[int] = 10

class CandidateResponse(BaseModel):
    name: str
    linkedin_url: str
    fit_score: float
    score_breakdown: dict
    outreach_message: str
    key_characteristics: List[str]

class JobResponse(BaseModel):
    job_id: str
    candidates_found: int
    top_candidates: List[CandidateResponse]

def extract_key_characteristics(profile_data, scores):
    """Extract key characteristics from candidate profile and scores"""
    characteristics = []
    
    # Education highlights
    if scores.get("education", 0) >= 7:
        education = profile_data.get("education", [])
        if education:
            top_school = education[0].get("school", "")
            characteristics.append(f"Graduated from {top_school}")
    
    # Company highlights
    if scores.get("company", 0) >= 8:
        experience = profile_data.get("experience", [])
        if experience:
            top_company = experience[0].get("company", "")
            characteristics.append(f"Experience at {top_company}")
    
    # Skills highlights
    if scores.get("skills", 0) >= 7:
        characteristics.append("Strong AI/ML background")
    
    # Location highlights
    if scores.get("location", 0) >= 8:
        characteristics.append("Located in Bay Area")
    
    # Experience highlights
    if scores.get("tenure", 0) >= 7:
        characteristics.append("Significant industry experience")
    
    return characteristics

@app.get("/")
async def root():
    return {
        "message": "LinkedIn Sourcing Agent API",
        "version": "1.0.0",
        "endpoints": {
            "/sourcing": "POST - Find candidates for a job description",
            "/health": "GET - API health check"
        },
        "usage": {
            "method": "POST",
            "endpoint": "/sourcing",
            "body": {
                "job_description": "Your job description here",
                "location": "Mountain View (optional)",
                "num_candidates": 10
            }
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/sourcing", response_model=JobResponse)
async def find_candidates(request: JobRequest):
    """
    Find top candidates for a job description and generate personalized outreach messages.
    
    - **job_description**: The job description to search for candidates
    - **location**: Preferred location (default: Mountain View)
    - **num_candidates**: Number of candidates to return (default: 10)
    """
    try:
        # Step 1: Search candidates
        candidates = search_candidates(
            request.job_description, 
            location=request.location, 
            num_results=request.num_candidates
        )
        
        if not candidates:
            raise HTTPException(status_code=404, detail="No candidates found for the given criteria")
        
        # Step 2: Score candidates
        scored = score_candidates(candidates, request.job_description)
        
        if not scored:
            raise HTTPException(status_code=500, detail="Failed to score candidates")
        
        # Step 3: Generate outreach messages
        messages = generate_messages(scored[:request.num_candidates], request.job_description)
        
        # Step 4: Create message lookup
        message_lookup = {msg["candidate"]: msg["message"] for msg in messages}
        
        # Step 5: Build response
        top_candidates = []
        for candidate in scored[:request.num_candidates]:
            # Extract key characteristics
            key_characteristics = extract_key_characteristics(
                candidate["profile"], 
                candidate["scores"]
            )
            
            candidate_response = CandidateResponse(
                name=candidate["candidate"],
                linkedin_url=candidate["linkedin_url"],
                fit_score=candidate["score"],
                score_breakdown=candidate["scores"],
                outreach_message=message_lookup.get(candidate["candidate"], "Message not generated"),
                key_characteristics=key_characteristics
            )
            top_candidates.append(candidate_response)
        
        # Generate job ID based on job description
        import hashlib
        job_id = hashlib.md5(request.job_description.encode()).hexdigest()[:8]
        
        response = JobResponse(
            job_id=f"job-{job_id}",
            candidates_found=len(candidates),
            top_candidates=top_candidates
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 