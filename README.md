Resume AI is a fast and simple tool for extracting and analyzing resume content using Python and Streamlit.  
It reads files (PDF, DOCX, images, or TXT), extracts the text using OCR or direct parsing, and analyzes it to identify:

- Name, Email, Phone number
- Technical Skills
- Education & Work Experience
- Languages

---

## Live Demo (Streamlit Interface)

![screenshot](![alt text](image.png)) <!-- Replace with actual screenshot -->

---

##  Features

- OCR support for scanned PDFs and images.
- Smart text extraction and parsing.
- Clean and responsive Streamlit interface.
- Download results as JSON or plain text.

---

##  Tech Stack

- Python 3.10+
- Streamlit
- Tesseract OCR
- PDFPlumber
- Pillow / pdf2image
- python-docx

---

##  Project Structure

```bash
resume-ai/
├── app.py                  # Streamlit interface
├── main.py                 # CLI version
├── modules/
│   ├── extractor.py        # Handles file reading and OCR
│   └── parser.py           # Parses resume data from raw text
├── outputs/                # Generated output files (JSON/TXT)
├── sample_data/            # Sample resumes
├── requirements.txt        # Required dependencies
└── README.md