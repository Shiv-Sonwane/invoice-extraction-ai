# 📄 Invoice Extraction AI

An AI-powered application that extracts structured data from invoice documents (images/PDFs), stores results in a database, and provides analytics.

---

## 🚀 Features

- 📤 Upload invoice files (JPG, PNG, PDF)
- 🔍 OCR-based text extraction using Tesseract
- 🤖 AI-powered parsing using Gemini (with fallback support)
- ✅ Structured JSON output
- 📊 Analytics dashboard:
  - Total invoices processed
  - Total spend
  - Vendor-wise spend
  - Monthly trends
- 🚫 Duplicate invoice detection
- 🎯 Confidence score for extracted data

---

## 🧠 How It Works

1. User uploads an invoice from the frontend  
2. Backend extracts text using OCR (Tesseract)  
3. Extracted text is processed using an AI model (Gemini)  
4. Data is converted into structured JSON  
5. Data is validated and stored in Supabase  
6. Analytics are generated from stored data  

---

## 🏗️ Tech Stack

### Frontend
- React (Vite)
- Axios

### Backend
- FastAPI
- Tesseract OCR
- pdf2image
- Gemini API

### Database
- Supabase (PostgreSQL + Storage)

### Deployment
- Frontend → Vercel  
- Backend → Railway  

---


# 📄 Invoice Extraction AI

An AI-powered application that extracts structured data from invoice documents (images/PDFs), stores results in a database, and provides analytics.

---

## 🚀 Features

- 📤 Upload invoice files (JPG, PNG, PDF)
- 🔍 OCR-based text extraction using Tesseract
- 🤖 AI-powered parsing using Gemini (with fallback support)
- ✅ Structured JSON output
- 📊 Analytics dashboard:
  - Total invoices processed
  - Total spend
  - Vendor-wise spend
  - Monthly trends
- 🚫 Duplicate invoice detection
- 🎯 Confidence score for extracted data

---

## 🧠 How It Works

1. User uploads an invoice from the frontend  
2. Backend extracts text using OCR (Tesseract)  
3. Extracted text is processed using an AI model (Gemini)  
4. Data is converted into structured JSON  
5. Data is validated and stored in Supabase  
6. Analytics are generated from stored data  

---

## 🏗️ Tech Stack

### Frontend
- React (Vite)
- Axios

### Backend
- FastAPI
- Tesseract OCR
- pdf2image
- Gemini API

### Database
- Supabase (PostgreSQL + Storage)

### Deployment
- Frontend → Vercel  
- Backend → render  

---

## 📂 Project Structure


### Backend
- FastAPI
- Tesseract OCR
- pdf2image
- Gemini API

### Database
- Supabase (PostgreSQL + Storage)

### Deployment
- Frontend → Vercel  
- Backend → Railway  

---

## 📂 Project Structure

project-root/
│
├── backend/
│ ├── main.py
│ ├── llm_parser.py
│ ├── ocr.py
│ ├── validator.py
│ ├── db.py
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ ├── App.jsx
│ └── App.css
│
└── README.md


---

## ⚙️ Setup Instructions

### 🔹 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### 🔹 frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 📊 API Endpoints

## Upload Invoice
 POST /upload

## Get Analytics
 GET /analytics


### 📈 Example Output
```bash
{
  "vendor_name": "ABC Pvt Ltd",
  "invoice_number": "INV-123",
  "invoice_date": "2023-05-10",
  "total_amount": 1500,
  "currency": "$"
}
```


### ⚠️ Assumptions & Limitations
-OCR accuracy depends on image quality
-Different invoice formats may affect extraction
-Free API limits may restrict AI usage
-Date formats may vary across invoices


### 🔮 Future Improvements
-Format detection & reuse system
-Batch invoice processing
-Improved UI with charts
-Vendor normalization


### 🌐 Live Demo
Frontend (Vercel): [Frontend](https://invoice-extraction-ai-two.vercel.app/)
Backend (Render): [Backend](https://invoice-extraction-ai-4h99.onrender.com/)
