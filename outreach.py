def generate_messages(scored_candidates, job_description):
    messages = []

    for candidate in scored_candidates:
        name = candidate["candidate"]
        profile = candidate["profile"]
        scores = candidate["scores"]
        
        # Extract key characteristics for personalization
        characteristics = []
        
        # Education highlights
        if scores.get("education", 0) >= 7:
            education = profile.get("education", [])
            if education:
                top_school = education[0].get("school", "")
                characteristics.append(f"your impressive education from {top_school}")
        
        # Company highlights
        if scores.get("company", 0) >= 8:
            experience = profile.get("experience", [])
            if experience:
                top_company = experience[0].get("company", "")
                characteristics.append(f"your experience at {top_company}")
        
        # Skills highlights
        if scores.get("skills", 0) >= 7:
            characteristics.append("your strong AI/ML background")
        
        # Location highlights
        if scores.get("location", 0) >= 8:
            characteristics.append("your Bay Area location")
        
        # Experience highlights
        if scores.get("tenure", 0) >= 7:
            characteristics.append("your significant industry experience")
        
        # Fallback if no specific characteristics
        if not characteristics:
            headline = profile.get("headline", "")
            if headline:
                characteristics.append(f"your background in {headline}")
            else:
                characteristics.append("your impressive background")
        
        # Create personalized message
        characteristics_text = ", ".join(characteristics)
        
        # Explain why they're a good fit
        fit_reasons = []
        if scores.get("skills", 0) >= 7:
            fit_reasons.append("your technical expertise aligns perfectly with our requirements")
        if scores.get("company", 0) >= 8:
            fit_reasons.append("your experience at top-tier companies shows the caliber we're looking for")
        if scores.get("location", 0) >= 8:
            fit_reasons.append("your location makes you an ideal candidate for our team")
        
        fit_explanation = ". ".join(fit_reasons) if fit_reasons else "your background makes you an excellent fit for this role"
        
        message = (
            f"Hi {name}, "
            f"We came across your profile and were really impressed by {characteristics_text}. "
            f"{fit_explanation.capitalize()}.\n\n"
            f"We're currently hiring for a role that we think you'd be a great fit for:\n\n"
            f"{job_description.strip()}\n\n"
            "Would you be open to a quick chat to discuss this opportunity?\n\n"
            "Thanks!"
        )
        
        messages.append({
            "candidate": name,
            "message": message
        })

    return messages