"""
Test Gemini 2.0 and experimental models
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🔍 TESTING GEMINI 2.0 & EXPERIMENTAL MODELS")
print("=" * 80)
print()

api_keys = {
    "FLASH": os.getenv("GEMINI_FLASH_KEY"),
    "PRO": os.getenv("GEMINI_PRO_KEY"),
    "LITE": os.getenv("GEMINI_LITE_KEY")
}

print("📋 API Keys Found:")
for name, key in api_keys.items():
    if key:
        print(f"   ✅ {name}: {key[:25]}...{key[-8:]}")
    else:
        print(f"   ❌ {name}: NOT FOUND")
print()

# Test configurations for Gemini 2.0 models
test_configs = [
    ("FLASH (Gemini 2.0 Flash Preview)", "FLASH", [
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash",
        "gemini-pro"
    ]),
    ("PRO (Gemini Exp 1206)", "PRO", [
        "gemini-exp-1206",
        "gemini-1.5-pro",
        "gemini-pro"
    ]),
    ("LITE (Gemini 2.0 Flash Lite)", "LITE", [
        "gemini-2.0-flash-lite-exp",
        "gemini-1.5-flash-8b",
        "gemini-flash"
    ])
]

print("🧪 Testing Each Model...")
print("-" * 80)

working_configs = []

for display_name, key_name, model_names in test_configs:
    print(f"\n{display_name}:")
    
    api_key = api_keys[key_name]
    if not api_key:
        print(f"   ❌ No API key found")
        continue
    
    for model in model_names:
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
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    print(f"✅ WORKS! Response: {text[:30]}")
                    working_configs.append((display_name, model, api_key))
                    break
            elif response.status_code == 403:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', '')
                if 'API_NOT_ENABLED' in error_msg or 'has not been used' in error_msg:
                    print(f"❌ API not enabled")
                else:
                    print(f"❌ {error_msg[:60]}")
            elif response.status_code == 404:
                print(f"❌ Model not found")
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")

print()
print("=" * 80)
print("📊 RESULTS")
print("=" * 80)
print()

if working_configs:
    print(f"✅ {len(working_configs)} working configuration(s) found!")
    print()
    for name, model, key in working_configs:
        print(f"   {name}:")
        print(f"      Model: {model}")
        print(f"      Key: {key[:25]}...{key[-8:]}")
    print()
    print("=" * 80)
    print("🎉 YOUR APP SHOULD WORK NOW!")
    print("=" * 80)
    print()
    print("Restart your backend:")
    print("   python main.py")
    print()
    print("Then test at: http://localhost:3002")
else:
    print("❌ NO WORKING CONFIGURATIONS FOUND")
    print()
    print("Solutions:")
    print()
    print("1. Get NEW API keys from AI Studio:")
    print("   → https://aistudio.google.com/app/apikey")
    print("   → Click 'Create API key'")
    print("   → Choose 'Create API key in NEW project'")
    print()
    print("2. Update backend/.env with the new key")
    print()
    print("3. Run this test again: python test_gemini_2.py")

print()
print("=" * 80)
