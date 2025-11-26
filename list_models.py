# list_models.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("Set GOOGLE_API_KEY in .env or environment")

genai.configure(api_key=API_KEY)

# Call list_models() to get model metadata
models = genai.list_models()   # SDK method that returns available models
print("Found models (first 2000 chars):")
print(models)                  # inspect raw output
