import os
import re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import json

# مسار Tesseract OCR (تأكد أنه صحيح عندك)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_any_file(file_path):
    """
    Extract text from PDF, images, Word, and text files with OCR fallback.
    """
    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    _, ext = os.path.splitext(file_path.lower())

    try:
        if ext == ".pdf":
            print("🧪 Trying pdfplumber for PDF text...")
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        page_text = page.extract_text()
                        print(f"📄 Page {i+1} → {'✅ Text found' if page_text else '❌ No text'}")
                        if page_text:
                            text += page_text + "\n"
                if text.strip():
                    return text
            except Exception as e:
                print(f"⚠️ pdfplumber failed: {e}")

            print("🔄 Trying OCR on PDF pages...")
            images = convert_from_path(file_path)
            text = ""
            for i, img in enumerate(images):
                print(f"🖼️ OCR Page {i+1}")
                text += pytesseract.image_to_string(img) + "\n"
            return text if text.strip() else "❌ OCR didn't find any text."

        elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"]:
            print("🖼️ Using OCR on image...")
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            return text if text.strip() else "❌ No text found in image."

        elif ext in [".docx", ".doc"]:
            print("📄 Reading Word document...")
            try:
                import docx
                doc = docx.Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])
                return text if text.strip() else "❌ No text found in Word file."
            except Exception as e:
                return f"❌ Error reading Word file: {e}"

        elif ext in [".txt", ".md", ".py", ".html", ".css", ".json", ".xml", ".js"]:
            print("📜 Reading text file...")
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()

        else:
            return f"❌ Unsupported file type: {ext}"

    except Exception as e:
        return f"❌ Error during processing: {e}"

def parse_resume_text(text):
    parsed_data = {}

    lines = text.split('\n')

    # الاسم
    parsed_data['Name'] = lines[0].strip() if lines else 'Not found'

    # الإيميل
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    parsed_data['Email'] = email_match.group() if email_match else 'Not found'

    # رقم الهاتف
    phone_match = re.search(r'(\+?\d[\d\s\-]{9,15})', text)
    parsed_data['Phone'] = phone_match.group() if phone_match else 'Not found'

    # المهارات
    skill_keywords = ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'HTML', 'CSS', 'AI', 'Machine Learning']
    skills_found = [skill for skill in skill_keywords if skill.lower() in text.lower()]
    parsed_data['Skills'] = skills_found if skills_found else 'Not found'

    # التعليم
    education_keywords = ['Bachelor', 'Master', 'B.Sc', 'M.Sc', 'University', 'Degree']
    education_lines = [line for line in lines if any(word in line for word in education_keywords)]
    parsed_data['Education'] = education_lines if education_lines else 'Not found'

    # الخبرة
    experience_keywords = ['experience', 'worked', 'intern', 'responsible', 'position']
    experience_lines = [line for line in lines if any(word.lower() in line.lower() for word in experience_keywords)]
    parsed_data['Experience'] = experience_lines if experience_lines else 'Not found'

    # اللغات
    lang_keywords = ['Arabic', 'English', 'French', 'German', 'Spanish']
    lang_lines = [line for line in lines if any(lang in line for lang in lang_keywords)]
    parsed_data['Languages'] = lang_lines if lang_lines else 'Not found'

    return parsed_data

def main():
    print("="*60)
    print("📄 CV Text Extractor & Parser (Ali's Project)")
    print("="*60)

    file_path = "E:\\resume_ai\\sample_data\\photo.png"

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    text = extract_text_from_any_file(file_path)

    print("\n" + "="*60)
    print("📝 Extracted Text (First 1000 characters):\n")
    print(text[:1000])  # You can remove this if you want full text

    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("\n✅ Text saved to extracted_text.txt")

    print("\n" + "="*60)
    print("🔍 Parsed Resume Information:\n")
    parsed = parse_resume_text(text)
    for key, value in parsed.items():
        print(f"\n🔹 {key}:")
        if isinstance(value, list):
            for item in value:
                print(f"   - {item}")
        else:
            print(f"   {value}")

    print("\n" + "="*60)
    print("🎯 Done! This is your CLI-based Resume Extractor.")

    with open("parsed_resume.json", "w", encoding="utf-8") as json_file:
        json.dump(parsed, json_file, indent=4, ensure_ascii=False)

    print("✅ Parsed data saved to parsed_resume.json")
    

if __name__ == "__main__":
    main()

