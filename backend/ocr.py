import pytesseract
from PIL import Image
import os

from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path: str):
    text = ""

    # 🔍 get extension safely
    ext = os.path.splitext(file_path)[1].lower()
    
    print(ext)
    
    # fallback: assume image if no extension
    if not ext:
        ext = ".jpg"

    # 🟢 IMAGE FILES
    if ext in [".jpg", ".jpeg", ".png"]:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    # 🟢 PDF FILES
    elif ext == ".pdf":
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    else:
        # 🔥 fallback: try opening as image anyway
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
        except:
            raise ValueError(f"Unsupported file format: {ext}")

    return text