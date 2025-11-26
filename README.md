🌡️✨ Gemini MedScan — AI-Powered Medical Report & Symptom Analyzer

Gemini MedScan is an AI-driven health assistant that analyzes medical scan images and symptom descriptions to give quick, reliable, first-level medical insights.
Built using Gemini 2.5 Flash, it bridges the gap between patients and early medical understanding.

🧠 Inspiration

Access to medical understanding is still slow, confusing, or limited. Many patients don't understand their scan reports, and symptoms often go unchecked until they worsen.
We wanted to create a fast, accessible, AI-powered tool that gives people clarity and helps them make informed health decisions instantly.

🚑 What It Does

✔️ Analyzes symptoms to identify possible diseases
✔️ Scans medical images (X-ray, MRI, Reports) using Gemini Vision
✔️ Provides:
1.Likely conditions
2.Severity estimation
3.First-aid steps
4.Advice on whether doctor consultation is needed
5.Clear, simple explanations
✔️ Real-time REST API for integration into apps or healthcare tools

🏗️ How We Built It

Backend built using Flask (Python)

Integrated Google’s Gemini 2.5 Flash + Image Preview Vision Model

Frontend (optional) using HTML, CSS, JavaScript

Secure environment handling using dotenv

Image upload & processing using Werkzeug

Cross-origin support through Flask-CORS

🧩 Challenges We Ran Into

Choosing the correct Gemini model ID for image analysis

Handling CORS issues in local + cloud environments

Ensuring accurate scan report interpretation

Fixing API version mismatches and 404 model errors

Optimizing prompts for medical clarity and safety

🏆 Accomplishments We’re Proud Of

1)Successfully integrated Gemini for medical image interpretation
2)Built a functional, scalable backend API
3)Created a smooth workflow for symptom + scan analysis
4)Achieved clean, structured medical outputs through prompt engineering

📚 What We Learned

Advanced usage of Generative AI with multimodal prompts

Model selection using ListModels

Error handling with real-time AI APIs

Best practices for building healthcare-related AI systems

Secure and modular backend architecture

🚀 What’s Next for Gemini MedScan

->Adding disease-risk scoring using AI
->Mobile app (Flutter / React Native)
->Support for multilingual analysis
->Integration with wearable health devices
->Doctor dashboard for detailed insights
->Real-time emergency alerts
->HIPAA-style privacy & encryption upgrades

🛠️ Built With

1)Gemini 2.5 Flash API
2)Gemini Vision (Image Preview Model)
3)Flask
4)Python
5)HTML
6)CSS
7)JavaScript
8)Google Generative AI SDK
9)dotenv
10)Werkzeug
11)GitHub
12)VS Code
