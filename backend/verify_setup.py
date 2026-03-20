"""
Verify your complete setup and find the exact issue
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🔍 COMPLETE SETUP VERIFICATION")
print("=" * 80)
print()

# Get API keys
api_keys = {
    "FLASH": os.getenv("GEMINI_FLASH_KEY"),
    "PRO": os.getenv("GEMINI_PRO_KEY"),
    "LITE": os.getenv("GEMINI_LITE_KEY")
}

print("1️⃣ Checking API Keys...")
print("-" * 80)
for name, key in api_keys.items():
    if key:
        print(f"✅ {name}: {key[:25]}...{key[-8:]}")
    else:
        print(f"❌ {name}: NOT FOUND")
print()

# Test each key with simple REST call
print("2️⃣ Testing API Keys with Direct REST Calls...")
print("-" * 80)

working_key = None
working_model = None

for key_name, api_key in api_keys.items():
    if not api_key:
        continue
    
    print(f"\nTesting {key_name}...")
    
    # Try different models
    models_to_try = [
        "gemini-pro",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash-8b"
    ]
    
    for model in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": "Say 'test'"}]
                }]
            }
            
            print(f"   Trying {model}...", end=" ")
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data:
                    print(f"✅ WORKS!")
                    working_key = api_key
                    working_model = model
                    break
            elif response.status_code == 400:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', '')
                if 'API_KEY_INVALID' in error_msg or 'API key not valid' in error_msg:
                    print(f"❌ Invalid API key")
                    break
                else:
                    print(f"❌ {error_msg[:50]}")
            elif response.status_code == 403:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', '')
                print(f"❌ {error_msg[:60]}")
                if 'API_NOT_ENABLED' in error_msg or 'has not been used' in error_msg:
                    print(f"      → API not enabled for this project")
                    print(f"      → Your key is from a different project!")
                break
            elif response.status_code == 404:
                print(f"❌ Model not found")
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")
    
    if working_key:
        break

print()
print("=" * 80)
print("📊 DIAGNOSIS")
print("=" * 80)
print()

if working_key:
    print(f"✅ SUCCESS! Found working configuration:")
    print(f"   Model: {working_model}")
    print(f"   Key: {working_key[:25]}...{working_key[-8:]}")
    print()
    print("Your app should work now. If not, restart the backend.")
else:
    print("❌ NO WORKING CONFIGURATION FOUND")
    print()
    print("🔍 DIAGNOSIS:")
    print()
    print("Your API keys are from a DIFFERENT Google Cloud project")
    print("than where you enabled the API.")
    print()
    print("=" * 80)
    print("🔧 SOLUTION - Get New API Keys from AI Studio")
    print("=" * 80)
    print()
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print()
    print("2. Click 'Create API key'")
    print()
    print("3. Choose 'Create API key in new project' (IMPORTANT!)")
    print("   This will create a project with API already enabled!")
    print()
    print("4. Copy the new API key")
    print()
    print("5. Update backend/.env with the NEW key:")
    print()
    print("   GEMINI_FLASH_KEY=your_new_key_here")
    print("   GEMINI_PRO_KEY=your_new_key_here")
    print("   GEMINI_LITE_KEY=your_new_key_here")
    print()
    print("   (Use the SAME key for all three)")
    print()
    print("6. Restart backend: python backend/main.py")
    print()
    print("=" * 80)
    print()
    print("💡 WHY THIS HAPPENS:")
    print()
    print("You have API keys from Project A")
    print("But you enabled the API in Project B")
    print("They need to be in the SAME project!")
    print()
    print("Creating a new key in AI Studio automatically creates")
    print("a project with the API already enabled.")
    print()

print("=" * 80)
