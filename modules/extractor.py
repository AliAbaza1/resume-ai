import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# حدد مسار Tesseract في جهازك (أو استخدم .env لاحقًا)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_text_from_any_file(file_path):
    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    _, ext = os.path.splitext(file_path.lower())

    try:
        if ext == ".pdf":
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                if text.strip():
                    return text
            except Exception:
                pass  # fallback to OCR below

            # fallback: OCR from image
            images = convert_from_path(file_path)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img) + "\n"
            return text if text.strip() else ""

        elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img)

        elif ext in [".txt", ".md", ".html", ".json"]:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        else:
            return f"❌ Unsupported file type: {ext}"

    except Exception as e:
        return f"❌ Error: {e}"
