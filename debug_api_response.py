import os
from dotenv import load_dotenv
from fetch_profile import fetch_profile_pdf
import json

load_dotenv()

def debug_api_response():
    """Debug the actual API response structure"""
    
    test_url = "https://www.linkedin.com/in/yunfanjiang71"
    
    print("🔍 Debugging API Response Structure...")
    print("=" * 50)
    
    # Fetch profile data
    profile_data = fetch_profile_pdf(test_url)
    
    if profile_data:
        print("✅ API Response received")
        print(f"Response keys: {list(profile_data.keys())}")
        
        # Print the full response structure
        print("\n📋 Full API Response:")
        print(json.dumps(profile_data, indent=2))
        
        # Check if there's nested data
        if 'data' in profile_data:
            print("\n🔍 Checking 'data' field:")
            data = profile_data['data']
            if data:
                print(f"Data keys: {list(data.keys())}")
                print("Data content:")
                print(json.dumps(data, indent=2))
            else:
                print("Data field is empty or None")
        
        # Look for education in different possible locations
        print("\n🔍 Searching for education data...")
        
        # Method 1: Direct access
        education = profile_data.get("education", [])
        print(f"Direct education access: {education}")
        
        # Method 2: Nested access
        if 'data' in profile_data and profile_data['data']:
            nested_education = profile_data['data'].get("education", [])
            print(f"Nested education access: {nested_education}")
        
        # Method 3: Search recursively
        def find_education_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if key.lower() in ['education', 'educations', 'school', 'university']:
                        print(f"Found potential education at {current_path}: {value}")
                    find_education_recursive(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    find_education_recursive(item, current_path)
        
        print("\n🔍 Recursive search for education data:")
        find_education_recursive(profile_data)
        
    else:
        print("❌ No profile data received")

if __name__ == "__main__":
    debug_api_response() 