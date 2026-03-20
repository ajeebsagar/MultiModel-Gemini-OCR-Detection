"""
Quick test script to verify the API is working correctly
Run this after starting the backend server
"""
import requests
import os

def test_health_check():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on port 8000?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_keys():
    """Check if API keys are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    keys = {
        "GEMINI_FLASH_KEY": os.getenv("GEMINI_FLASH_KEY"),
        "GEMINI_PRO_KEY": os.getenv("GEMINI_PRO_KEY"),
        "GEMINI_LITE_KEY": os.getenv("GEMINI_LITE_KEY")
    }
    
    all_present = True
    for key_name, key_value in keys.items():
        if key_value:
            print(f"✅ {key_name} is configured")
        else:
            print(f"❌ {key_name} is missing!")
            all_present = False
    
    return all_present

def main():
    print("=" * 60)
    print("🧪 OCR Document Analysis - API Test")
    print("=" * 60)
    print()
    
    print("1. Testing API Keys Configuration...")
    keys_ok = test_api_keys()
    print()
    
    print("2. Testing Backend Health...")
    backend_ok = test_health_check()
    print()
    
    print("=" * 60)
    if keys_ok and backend_ok:
        print("✅ ALL TESTS PASSED!")
        print()
        print("Next steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Upload an image with text")
        print("3. Click 'Analyze Document'")
        print("4. View OCR results from all three models")
    else:
        print("❌ SOME TESTS FAILED")
        print()
        if not keys_ok:
            print("Fix: Check your backend/.env file has all API keys")
        if not backend_ok:
            print("Fix: Start the backend with: python main.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
