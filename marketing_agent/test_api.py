"""Test script to verify Gemini API key loading."""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

print("="*60)
print("API KEY VERIFICATION")
print("="*60)
print(f"\nAPI Key found: {api_key is not None}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"API Key starts with: {api_key[:10] if api_key else 'N/A'}...")
print(f"API Key ends with: ...{api_key[-5:] if api_key else 'N/A'}")

# Check for whitespace issues
if api_key:
    print(f"\nHas leading whitespace: {api_key != api_key.lstrip()}")
    print(f"Has trailing whitespace: {api_key != api_key.rstrip()}")
    
    # Test with stripped key
    clean_key = api_key.strip()
    print(f"\nCleaned key length: {len(clean_key)}")
    
    # Try to initialize Gemini
    try:
        import google.generativeai as genai
        print("\nAttempting to initialize Gemini with cleaned key...")
        genai.configure(api_key=clean_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Test the model
        response = model.generate_content("Hello, are you working?")
        print(f"\n✅ SUCCESS! API key is valid!")
        print(f"Response: {response.text[:100]}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPossible issues:")
        print("1. API key might be expired or revoked")
        print("2. API key might not have proper permissions")
        print("3. Network connectivity issue")
        print("\nTry getting a fresh API key from:")
        print("https://makersuite.google.com/app/apikey")
else:
    print("\n❌ API key not found in environment!")
    print("Check that .env file exists and contains:")
    print("GEMINI_API_KEY=your-key-here")

print("\n" + "="*60)
