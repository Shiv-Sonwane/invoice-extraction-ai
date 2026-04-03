# from fastapi import FastAPI, UploadFile, File
# import os
# from ocr import extract_text
# from llm_parser import parse_invoice, calculate_confidence
# from validator import validate_invoice
# from db import supabase
# from collections import defaultdict

# app = FastAPI()



# # Create uploads folder if not exists
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.get("/")
# def home():
#     return {"message": "Backend is running 🚀"}

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = f"{UPLOAD_DIR}/{file.filename}"

#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     # OCR
#     text = extract_text(file_path)

#     # parsing
#     structured_data = parse_invoice(text)

#     # Validation
#     data = validate_invoice(structured_data)

#     confidence = calculate_confidence(data)

#     #duplicate check
#     existing = supabase.table("invoices") \
#        .select("*") \
#        .eq("invoice_number", data["invoice_number"]) \
#        .eq("vendor_name", data["vendor_name"]) \
#        .execute()

#     if existing.data:
#         return {
#            "message": "Duplicate invoice detected",
#            "data": data,
#            "confidence": confidence
#         }

#     supabase.table("invoices").insert({
#        "vendor_name": data["vendor_name"],
#        "invoice_number": data["invoice_number"],
#        "invoice_date": data["invoice_date"],
#        "total_amount": data["total_amount"],
#        "currency": data["currency"],
#        "file_url": file_path
#     }).execute()

#     return {
#         "structured_data": data
#     }

# @app.get("/analytics")
# def get_analytics():
#     response = supabase.table("invoices").select("*").execute()
#     invoices = response.data

#     total_invoices = len(invoices)
#     total_spend = 0

#     vendor_spend = defaultdict(float)
#     monthly_spend = defaultdict(float)

#     for inv in invoices:
#         try:
#             amount = float(inv.get("total_amount") or 0)
#         except:
#             amount = 0

#         total_spend += amount

#         # vendor
#         vendor = inv.get("vendor_name") or "Unknown"
#         vendor_spend[vendor] += amount

#         # month (make safer)
#         date = inv.get("invoice_date")
#         if date and isinstance(date, str):
#             month = date[:7]
#             monthly_spend[month] += amount

#     return {
#         "total_invoices": total_invoices,
#         "total_spend": total_spend,
#         "by_vendor": dict(vendor_spend),
#         "monthly_trends": dict(monthly_spend)
#     }

from fastapi import FastAPI, UploadFile, File
import os
import uuid
from ocr import extract_text
from llm_parser import parse_invoice, calculate_confidence
from validator import validate_invoice
from db import supabase
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# temp folder for OCR
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    # ✅ Step 0: Validate file type
    allowed_extensions = [".jpg", ".jpeg", ".png", ".webp", ".pdf"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        return {
            "error": f"Unsupported file format: {ext}. Please upload JPG, PNG, WEBP or PDF."
        }

    # fallback if extension missing
    if not ext:
        ext = ".jpg"

    # ✅ Step 1: Save temp file for OCR
    temp_path = f"{UPLOAD_DIR}/{uuid.uuid4()}{ext}"

    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    # ✅ Step 2: OCR
    text = extract_text(temp_path)

    # ✅ Step 3: LLM parsing
    structured_data = parse_invoice(text)

    # handle LLM error
    if "error" in structured_data:
        return {"error": "LLM parsing failed", "details": structured_data["error"]}

    # ✅ Step 4: Validation
    data = validate_invoice(structured_data)

    # ✅ Step 5: Confidence
    confidence = calculate_confidence(data)

    # ✅ Step 6: Duplicate check
    existing = supabase.table("invoices") \
        .select("*") \
        .eq("invoice_number", data["invoice_number"]) \
        .eq("vendor_name", data["vendor_name"]) \
        .execute()

    if existing.data:
        return {
            "message": "Duplicate invoice detected",
            "data": data,
            "confidence": confidence
        }

    # ✅ Step 7: Upload to Supabase Storage
    file_name = f"{uuid.uuid4()}-{file.filename}"

    supabase.storage.from_("invoices").upload(
        file_name,
        file_bytes
    )

    file_url = supabase.storage.from_("invoices").get_public_url(file_name)

    # ✅ Step 8: Save to DB
    supabase.table("invoices").insert({
        "vendor_name": data["vendor_name"],
        "invoice_number": data["invoice_number"],
        "invoice_date": data["invoice_date"],
        "total_amount": data["total_amount"],
        "currency": data["currency"],
        "file_url": file_url
    }).execute()

    return {
        "structured_data": data,
        "confidence": confidence,
        "file_url": file_url,
        "duplicate": False
    }


@app.get("/analytics")
def get_analytics():
    response = supabase.table("invoices").select("*").execute()
    invoices = response.data

    total_invoices = len(invoices)
    total_spend = 0

    vendor_spend = defaultdict(float)
    monthly_spend = defaultdict(float)

    for inv in invoices:
        try:
            amount = float(inv.get("total_amount") or 0)
        except:
            amount = 0

        total_spend += amount

        vendor = inv.get("vendor_name") or "Unknown"
        vendor_spend[vendor] += amount

        date = inv.get("invoice_date")
        if date and isinstance(date, str):
            month = date[:7]
            monthly_spend[month] += amount

    return {
        "total_invoices": total_invoices,
        "total_spend": total_spend,
        "by_vendor": dict(vendor_spend),
        "monthly_trends": dict(monthly_spend)
    }