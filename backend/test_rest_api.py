"""
Test Gemini API using direct REST calls
This bypasses the SDK to see if the API keys work at all
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🌐 TESTING GEMINI API VIA REST")
print("=" * 80)
print()

api_keys = {
    "FLASH": os.getenv("GEMINI_FLASH_KEY"),
    "PRO": os.getenv("GEMINI_PRO_KEY"),
    "LITE": os.getenv("GEMINI_LITE_KEY")
}

# Test models
models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro"
]

print("Testing API keys with REST API...")
print()

for key_name, api_key in api_keys.items():
    if not api_key:
        print(f"❌ {key_name}: No API key")
        continue
    
    print(f"Testing {key_name} ({api_key[:20]}...{api_key[-10:]})")
    print("-" * 80)
    
    for model in models_to_test:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Say 'test'"
                }]
            }]
        }
        
        try:
            print(f"   Trying {model}...", end=" ")
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    print(f"✅ WORKS! Response: {text[:30]}")
                    print(f"      → Use this model: {model}")
                    break
                else:
                    print(f"⚠️  Response but no content")
            elif response.status_code == 400:
                print(f"❌ Bad request")
            elif response.status_code == 403:
                error_data = response.json()
                print(f"❌ Permission denied: {error_data.get('error', {}).get('message', 'Unknown')[:60]}")
            elif response.status_code == 404:
                print(f"❌ Model not found")
            else:
                print(f"❌ Status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout")
        except Exception as e:
            print(f"❌ Error: {str(e)[:60]}")
    
    print()

print("=" * 80)
print()
print("💡 NEXT STEPS:")
print()
print("If all tests failed:")
print("1. Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
print("2. Make sure 'Generative Language API' is ENABLED")
print("3. Check billing: https://console.cloud.google.com/billing")
print("4. Create new API keys: https://aistudio.google.com/app/apikey")
print()
print("=" * 80)
