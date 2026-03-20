"""
Script to check available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def check_available_models():
    """List all available Gemini models"""
    api_key = os.getenv("GEMINI_FLASH_KEY")
    
    if not api_key:
        print("❌ No API key found in .env file")
        return
    
    try:
        genai.configure(api_key=api_key)
        print("🔍 Checking available Gemini models...\n")
        
        models = genai.list_models()
        
        print("Available models that support generateContent:\n")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"✅ {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description}")
                print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_available_models()
