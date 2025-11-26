# list_models_verbose.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("Set GOOGLE_API_KEY in .env or environment")

genai.configure(api_key=API_KEY)

print("Listing available models (this may take a second)...\n")

# genai.list_models() returns a generator or iterable of model objects.
models_iter = genai.list_models()

count = 0
for m in models_iter:
    count += 1
    print(f"----- MODEL #{count} -----")
    # Try to print obvious attributes safely
    try:
        # many SDK objects have .name or .id; print both if available
        name = getattr(m, "name", None) or getattr(m, "id", None) or getattr(m, "model", None)
        print("name/id/model:", name)
    except Exception:
        pass

    # Print full repr to inspect structure
    try:
        # some SDK objects are dataclasses/objects; try converting to dict/json
        try:
            d = m.__dict__
            print("object __dict__ keys:", list(d.keys()))
        except Exception:
            print("repr:", repr(m)[:1000])
    except Exception:
        print("Could not introspect model object; repr fallback:")
        print(repr(m)[:1000])
    print()
print(f"Total models iterated: {count}")
