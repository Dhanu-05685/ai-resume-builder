import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Get your API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {api_key[:10]}...") if api_key else print("❌ No API key found")

# Configure
genai.configure(api_key=api_key)

# Try to list available models
try:
    print("\n📋 Available Models:")
    for model in genai.list_models():
        print(f"  - {model.name}")
except Exception as e:
    print(f"❌ Error listing models: {e}")

# Try basic generation
try:
    print("\n🤖 Testing Model Generation:")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello World'")
    print(f"✅ Success: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")