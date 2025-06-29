import os
import requests
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def fetch_profile_pdf(linkedin_url):
    url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-profile-pdf-cv"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "fresh-linkedin-profile-data.p.rapidapi.com"
    }

    params = {
        "linkedin_url": linkedin_url
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print(f"Profile data retrieved for {linkedin_url}")
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error fetching profile for {linkedin_url}: {str(e)}")
        return None