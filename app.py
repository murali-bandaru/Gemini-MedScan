# app.py — corrected MedScan AI backend (Flask + Google Generative AI)
import os
import base64
import mimetypes
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import google.generativeai as genai

# load .env and environment variables
load_dotenv()

# create app
app = Flask(__name__)
CORS(app)

# Read API key from environment
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # Helpful error early so you see it immediately when starting server
    raise RuntimeError("No API key found. Set GOOGLE_API_KEY in .env or environment variables.")

# configure SDK
genai.configure(api_key=API_KEY)

# Choose model ids (use exact strings returned by list_models_verbose.py)
IMAGE_MODEL_ID = "models/gemini-2.5-flash-image-preview"
TEXT_MODEL_ID = "models/gemini-2.5-flash"  # fallback; replace if your list shows different

# Helper: encode file bytes to base64 payload expected by SDK
def encode_file_for_gemini(path):
    with open(path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode("utf-8")
    # guess mime type
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "application/octet-stream"
    return {"mime_type": mime_type, "data": encoded}

# --- Test route to verify model & auth quickly ---
@app.route("/_test_model", methods=["GET"])
def _test_model():
    try:
        # Test TEXT model first
        try:
            m = genai.GenerativeModel(TEXT_MODEL_ID)
            r = m.generate_content("Hello from MedScan AI — test. Give a short greeting.")
            return jsonify({"ok": True, "model": TEXT_MODEL_ID, "text": r.text[:500]})
        except Exception as e_text:
            # If text model fails, try image model with a text prompt (some models accept text-only)
            try:
                m2 = genai.GenerativeModel(IMAGE_MODEL_ID)
                r2 = m2.generate_content(["Test: Describe what you would do when given an image."])
                return jsonify({"ok": True, "model": IMAGE_MODEL_ID, "text": r2.text[:500]})
            except Exception as e_img:
                return jsonify({"ok": False, "errors": {"text_model": str(e_text), "image_model": str(e_img)}}), 500
    except Exception as err:
        return jsonify({"ok": False, "error": str(err)}), 500

# --- Analyze simple symptom text (frontend -> backend -> Gemini text model) ---
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)
        symptoms = data.get("symptoms", "").strip()
        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400

        prompt = (
            "You are a careful medical analysis assistant. "
            "Given the patient's symptoms below, provide (in simple language):\n"
            "1) Possible causes (brief list)\n"
            "2) Severity level (low/medium/high) and why\n"
            "3) Immediate first-aid recommendations\n"
            "4) Whether the user should see a doctor urgently\n\n"
            f"Symptoms: {symptoms}\n\n"
            "Return a clear, concise, human-friendly text answer."
        )

        model = genai.GenerativeModel(TEXT_MODEL_ID)
        result = model.generate_content(prompt)
        return jsonify({"analysis": result.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Upload & analyze a medical report image/PDF ---
@app.route("/scan-report", methods=["POST"])
def scan_report():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        uploads_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath)

        # Prepare encoded payload
        file_payload = encode_file_for_gemini(filepath)

        # Build prompt + file payload according to SDK pattern
        prompt = [
            "Analyze the attached medical scan or report. Extract key findings, list abnormal values (if any), "
            "explain in plain language, and suggest reasonable next steps to discuss with a clinician. "
            "Do not provide a diagnosis; advise to consult a licensed medical professional.",
            file_payload
        ]

        # Use image-capable model
        model = genai.GenerativeModel(IMAGE_MODEL_ID)
        response = model.generate_content(prompt)

        # Optionally remove uploaded file after processing (demo purposes)
        try:
            os.remove(filepath)
        except Exception:
            pass

        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health / root
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "MedScan AI Backend Running"})

if __name__ == "__main__":
    # run on 0.0.0.0 if you plan to access from other machines, otherwise 127.0.0.1 is fine
    app.run(host="127.0.0.1", port=5000, debug=True)
