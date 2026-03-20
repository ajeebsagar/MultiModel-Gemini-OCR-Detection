"""
Find the correct model names for your API keys
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🔍 FINDING CORRECT MODEL NAMES FOR YOUR API KEYS")
print("=" * 80)
print()

api_keys = {
    "FLASH": os.getenv("GEMINI_FLASH_KEY"),
    "PRO": os.getenv("GEMINI_PRO_KEY"),
    "LITE": os.getenv("GEMINI_LITE_KEY")
}

# All possible Gemini model names to try
all_models = [
    # Gemini 3.0 / 2.0 experimental
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-flash-lite-exp",
    "gemini-exp-1206",
    "gemini-exp-1121",
    "gemini-exp-1114",
    
    # Gemini 1.5
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest",
    
    # Gemini Pro
    "gemini-pro",
    "gemini-pro-vision",
    "gemini-flash",
    
    # With models/ prefix
    "models/gemini-2.0-flash-exp",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-pro",
]

print("Testing each API key with all possible model names...")
print()

working_configs = {}

for key_name, api_key in api_keys.items():
    if not api_key:
        print(f"❌ {key_name}: No API key found")
        continue
    
    print(f"Testing {key_name} ({api_key[:20]}...{api_key[-8:]})")
    print("-" * 80)
    
    found = False
    for model in all_models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": "Say 'test'"}]
                }]
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    print(f"   ✅ WORKS: {model}")
                    print(f"      Response: {text[:40]}")
                    working_configs[key_name] = model
                    found = True
                    break
                    
        except Exception:
            pass
    
    if not found:
        print(f"   ❌ No working model found for this key")
    
    print()

print("=" * 80)
print("📊 RESULTS")
print("=" * 80)
print()

if len(working_configs) == 3:
    print("✅ ALL THREE API KEYS WORK!")
    print()
    print("Working configurations:")
    for key, model in working_configs.items():
        print(f"   {key}: {model}")
    print()
    print("=" * 80)
    print("💡 UPDATE YOUR CODE")
    print("=" * 80)
    print()
    print("Copy this into backend/main.py MODELS section:")
    print()
    print("MODELS = {")
    print(f'    "flash": {{')
    print(f'        "name": "{working_configs.get("FLASH", "gemini-2.0-flash-exp")}",')
    print(f'        "api_key": os.getenv("GEMINI_FLASH_KEY"),')
    print(f'        "display_name": "Gemini 3 Flash Preview"')
    print(f'    }},')
    print(f'    "pro": {{')
    print(f'        "name": "{working_configs.get("PRO", "gemini-exp-1206")}",')
    print(f'        "api_key": os.getenv("GEMINI_PRO_KEY"),')
    print(f'        "display_name": "Gemini 3.1 Pro Preview"')
    print(f'    }},')
    print(f'    "lite": {{')
    print(f'        "name": "{working_configs.get("LITE", "gemini-2.0-flash-lite-exp")}",')
    print(f'        "api_key": os.getenv("GEMINI_LITE_KEY"),')
    print(f'        "display_name": "Gemini 3.1 Flash Lite Preview"')
    print(f'    }}')
    print("}")
    
elif len(working_configs) > 0:
    print(f"⚠️  {len(working_configs)} out of 3 API keys work")
    print()
    print("Working:")
    for key, model in working_configs.items():
        print(f"   ✅ {key}: {model}")
    print()
    print("Not working:")
    for key in ["FLASH", "PRO", "LITE"]:
        if key not in working_configs:
            print(f"   ❌ {key}")
    
else:
    print("❌ NONE OF YOUR API KEYS WORK")
    print()
    print("This means the Generative Language API is not enabled")
    print("for the projects these keys belong to.")
    print()
    print("SOLUTION:")
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print("2. Create THREE new API keys (one for each model)")
    print("3. Choose 'Create API key in NEW project' each time")
    print("4. Update backend/.env with the new keys")

print()
print("=" * 80)
