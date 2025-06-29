import requests
import json

def test_api():
    """Test the LinkedIn Sourcing Agent API"""
    
    # API endpoint (change this to your Hugging Face Space URL when deployed)
    base_url = "http://localhost:8000"
    
    # Test health check
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test root endpoint
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return
    
    # Test sourcing endpoint
    print("\n🔍 Testing sourcing endpoint...")
    
    test_job = {
        "job_description": "We're looking for a Senior Machine Learning Engineer with experience in LLMs, transformers, and code generation. The ideal candidate should have 3+ years of experience in AI/ML and be located in the Bay Area.",
        "location": "Mountain View",
        "num_candidates": 3
    }
    
    try:
        response = requests.post(
            f"{base_url}/sourcing",
            json=test_job,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Sourcing endpoint: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Found {result['candidates_found']} candidates")
            print(f"Job ID: {result['job_id']}")
            
            print("\n📋 Top Candidates:")
            for i, candidate in enumerate(result['top_candidates'], 1):
                print(f"\n{i}. {candidate['name']}")
                print(f"   Score: {candidate['fit_score']}/10")
                print(f"   LinkedIn: {candidate['linkedin_url']}")
                print(f"   Characteristics: {', '.join(candidate['key_characteristics'])}")
                print(f"   Message: {candidate['outreach_message'][:100]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"Sourcing endpoint failed: {e}")

if __name__ == "__main__":
    test_api() 