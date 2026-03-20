"""
Test script to verify Gemini API keys and available models
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("🔍 TESTING GEMINI API KEYS AND MODELS")
print("=" * 70)
print()

# Check if API keys are loaded
print("1️⃣ Checking API Keys in .env file...")
print("-" * 70)

keys = {
    "GEMINI_FLASH_KEY": os.getenv("GEMINI_FLASH_KEY"),
    "GEMINI_PRO_KEY": os.getenv("GEMINI_PRO_KEY"),
    "GEMINI_LITE_KEY": os.getenv("GEMINI_LITE_KEY")
}

all_keys_present = True
for key_name, key_value in keys.items():
    if key_value:
        # Show first 20 and last 5 characters
        masked = f"{key_value[:20]}...{key_value[-5:]}" if len(key_value) > 25 else key_value
        print(f"✅ {key_name}: {masked}")
    else:
        print(f"❌ {key_name}: NOT FOUND")
        all_keys_present = False

print()

if not all_keys_present:
    print("❌ Some API keys are missing! Check your backend/.env file")
    exit(1)

# Try to import and test the API
print("2️⃣ Testing Gemini API Connection...")
print("-" * 70)

try:
    import google.generativeai as genai
    print("✅ google.generativeai module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import google.generativeai: {e}")
    print("   Run: pip install google-generativeai")
    exit(1)

print()

# Test each API key
print("3️⃣ Testing Each API Key...")
print("-" * 70)

test_models = [
    ("FLASH", "GEMINI_FLASH_KEY", "gemini-1.5-flash"),
    ("PRO", "GEMINI_PRO_KEY", "gemini-1.5-pro"),
    ("LITE", "GEMINI_LITE_KEY", "gemini-1.5-flash-8b"),
]

working_models = []

for display_name, key_name, model_name in test_models:
    api_key = keys[key_name]
    print(f"\nTesting {display_name} ({model_name})...")
    
    try:
        genai.configure(api_key=api_key)
        
        # Try to create model instance
        model = genai.GenerativeModel(model_name)
        
        # Try a simple generation
        response = model.generate_content("Say 'test'")
        
        if response.text:
            print(f"✅ {display_name} API Key WORKS!")
            print(f"   Model: {model_name}")
            print(f"   Response: {response.text[:50]}...")
            working_models.append((display_name, model_name))
        else:
            print(f"⚠️  {display_name} API Key works but no response")
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ {display_name} FAILED: {error_msg}")
        
        # Try alternative model names
        alternatives = [
            f"models/{model_name}",
            model_name.replace("-", "_"),
            f"{model_name}-latest",
        ]
        
        print(f"   Trying alternatives...")
        for alt_name in alternatives:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(alt_name)
                response = model.generate_content("Say 'test'")
                if response.text:
                    print(f"   ✅ WORKS with: {alt_name}")
                    working_models.append((display_name, alt_name))
                    break
            except:
                print(f"   ❌ Failed: {alt_name}")

print()
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)

if working_models:
    print(f"✅ {len(working_models)} model(s) working:")
    for name, model in working_models:
        print(f"   • {name}: {model}")
    print()
    print("💡 Update backend/main.py with these model names!")
else:
    print("❌ No models working!")
    print()
    print("Possible issues:")
    print("1. API keys are invalid or expired")
    print("2. API keys don't have access to these models")
    print("3. Billing not enabled in Google Cloud")
    print("4. Rate limit exceeded")
    print()
    print("Solutions:")
    print("• Verify keys at: https://aistudio.google.com/app/apikey")
    print("• Check billing: https://console.cloud.google.com/billing")
    print("• Generate new API keys if needed")

print("=" * 70)
