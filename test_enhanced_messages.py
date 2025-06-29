import requests
import json

def test_enhanced_messages():
    """Test the enhanced outreach messages with key characteristics"""
    
    base_url = "http://localhost:8000"
    
    # Test job description
    test_job = {
        "job_description": "We're looking for a Senior Machine Learning Engineer with 3+ years of experience in LLMs, transformers, and code generation. The ideal candidate should have experience at top tech companies and be located in the Bay Area. This role involves training large language models for code generation at a Forbes AI 50 company.",
        "location": "Mountain View",
        "num_candidates": 2
    }
    
    print("🔍 Testing Enhanced Outreach Messages...")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{base_url}/sourcing",
            json=test_job,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result['candidates_found']} candidates")
            print(f"📋 Job ID: {result['job_id']}")
            
            print("\n" + "=" * 60)
            print("🎯 ENHANCED OUTREACH MESSAGES")
            print("=" * 60)
            
            for i, candidate in enumerate(result['top_candidates'], 1):
                print(f"\n{i}. {candidate['name']}")
                print(f"   Score: {candidate['fit_score']}/10")
                print(f"   LinkedIn: {candidate['linkedin_url']}")
                
                print(f"\n   📊 Score Breakdown:")
                for category, score in candidate['score_breakdown'].items():
                    print(f"      {category.capitalize()}: {score}/10")
                
                print(f"\n   🔑 Key Characteristics:")
                if candidate['key_characteristics']:
                    for char in candidate['key_characteristics']:
                        print(f"      • {char}")
                else:
                    print("      • No specific characteristics extracted")
                
                print(f"\n   💬 Enhanced Outreach Message:")
                print(f"      {candidate['outreach_message']}")
                
                print("\n" + "-" * 60)
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_enhanced_messages() 