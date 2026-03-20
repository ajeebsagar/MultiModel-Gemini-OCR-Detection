"""
Direct test of Gemini API with your keys
Run this to see exactly what's wrong
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🔍 DIRECT GEMINI API TEST")
print("=" * 80)
print()

# Test import
try:
    import google.generativeai as genai
    print("✅ google.generativeai imported successfully")
    print(f"   Version: {genai.__version__ if hasattr(genai, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"❌ Cannot import google.generativeai: {e}")
    print("   Run: pip install google-generativeai")
    exit(1)

print()

# Get API keys
api_keys = {
    "FLASH": os.getenv("GEMINI_FLASH_KEY"),
    "PRO": os.getenv("GEMINI_PRO_KEY"),
    "LITE": os.getenv("GEMINI_LITE_KEY")
}

print("📋 API Keys Found:")
for name, key in api_keys.items():
    if key:
        print(f"   ✅ {name}: {key[:20]}...{key[-10:]}")
    else:
        print(f"   ❌ {name}: NOT FOUND")

print()
print("=" * 80)
print("🧪 TESTING EACH MODEL")
print("=" * 80)

# Models to test
test_configs = [
    ("FLASH", "GEMINI_FLASH_KEY", [
        "gemini-1.5-flash",
        "models/gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro",
        "models/gemini-pro"
    ]),
    ("PRO", "GEMINI_PRO_KEY", [
        "gemini-1.5-pro",
        "models/gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-pro",
        "models/gemini-pro"
    ]),
    ("LITE", "GEMINI_LITE_KEY", [
        "gemini-1.5-flash-8b",
        "models/gemini-1.5-flash-8b",
        "gemini-1.5-flash-8b-latest",
        "gemini-flash",
        "models/gemini-flash"
    ])
]

working_configs = []

for display_name, key_name, model_names in test_configs:
    print()
    print(f"Testing {display_name}...")
    print("-" * 80)
    
    api_key = api_keys[display_name]
    if not api_key:
        print(f"❌ No API key found for {display_name}")
        continue
    
    genai.configure(api_key=api_key)
    
    # Try each model name
    for model_name in model_names:
        try:
            print(f"   Trying: {model_name}...", end=" ")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'test'")
            
            if response and response.text:
                print(f"✅ WORKS!")
                print(f"      Response: {response.text[:50]}")
                working_configs.append((display_name, model_name, api_key))
                break  # Found working config, move to next
            else:
                print(f"⚠️  No response")
        except Exception as e:
            error_str = str(e)
            if "API key not valid" in error_str or "invalid" in error_str.lower():
                print(f"❌ Invalid API key")
            elif "404" in error_str or "not found" in error_str.lower():
                print(f"❌ Model not found")
            elif "403" in error_str or "permission" in error_str.lower():
                print(f"❌ Permission denied")
            elif "billing" in error_str.lower():
                print(f"❌ Billing not enabled")
            else:
                print(f"❌ {error_str[:60]}")

print()
print("=" * 80)
print("📊 RESULTS")
print("=" * 80)

if working_configs:
    print(f"✅ {len(working_configs)} working configuration(s) found!")
    print()
    for name, model, key in working_configs:
        print(f"   {name}:")
        print(f"      Model: {model}")
        print(f"      Key: {key[:20]}...{key[-10:]}")
    
    print()
    print("=" * 80)
    print("💡 UPDATE YOUR CODE")
    print("=" * 80)
    print()
    print("Update backend/main.py MODELS configuration:")
    print()
    print("MODELS = {")
    for name, model, key in working_configs:
        model_key = name.lower()
        print(f'    "{model_key}": {{')
        print(f'        "name": "{model}",')
        print(f'        "api_key": os.getenv("GEMINI_{name}_KEY"),')
        print(f'        "display_name": "Gemini {name}"')
        print(f'    }},')
    print("}")
    
else:
    print("❌ NO WORKING CONFIGURATIONS FOUND!")
    print()
    print("Possible issues:")
    print()
    print("1. API Keys Invalid")
    print("   → Go to: https://aistudio.google.com/app/apikey")
    print("   → Create new API keys")
    print()
    print("2. Generative Language API Not Enabled")
    print("   → Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
    print("   → Click 'Enable'")
    print()
    print("3. Billing Not Enabled")
    print("   → Go to: https://console.cloud.google.com/billing")
    print("   → Link a billing account")
    print()
    print("4. Wrong Google Cloud Project")
    print("   → Make sure API keys are from the same project")
    print("   → Check project at: https://console.cloud.google.com/")
    print()
    print("5. API Restrictions")
    print("   → Go to: https://console.cloud.google.com/apis/credentials")
    print("   → Check API key restrictions")
    print("   → Allow 'Generative Language API'")

print()
print("=" * 80)
