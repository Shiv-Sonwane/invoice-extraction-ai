import os
from google import genai
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parse_invoice(text: str):
    prompt = f"""
Extract structured data from this invoice text.

IMPORTANT:
- "Invoice No", "Invoice Number", "No", "Bill No" all refer to invoice_number
- Return ONLY valid JSON (no explanation)

Format:
{{ 
  "vendor_name": "",
  "invoice_number": "",
  "invoice_date": "",
  "total_amount": "",
  "currency": ""
}}

Text:
{text}
"""
    models = [
        "models/gemini-flash-latest",   # primary
        "models/gemini-2.0-flash",      # fallback
        "models/gemini-pro-latest"      # backup
    ]
    


    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            content = response.text
            content = content.replace("```json", "").replace("```", "").strip()

            return json.loads(content)

        except Exception as e:
            print(f"Model {model} failed:", e)
            continue

    return {"error": "All models failed"}

def calculate_confidence(data):
    score = 0
    total = 5

    if data.get("vendor_name"): score += 1
    if data.get("invoice_number"): score += 1
    if data.get("invoice_date"): score += 1
    if data.get("total_amount"): score += 1
    if data.get("currency"): score += 1

    return round(score / total, 2)