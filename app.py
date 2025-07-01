import streamlit as st
import os
import json
from modules.extractor import extract_text_from_any_file
from modules.parser import parse_resume_text

st.set_page_config(page_title="CV Extractor", layout="wide")
st.title("📄 CV Extractor & Analyzer by Ali")

st.markdown("Upload a resume file (PDF, DOCX, TXT, or Image) and get instant insights.")

uploaded_file = st.file_uploader("📤 Upload your CV file", type=["pdf", "docx", "txt", "jpg", "png"])

if uploaded_file:
    os.makedirs("temp", exist_ok=True)
    save_path = os.path.join("temp", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ File uploaded successfully.")

    with st.spinner("🧠 Extracting text..."):
        text = extract_text_from_any_file(save_path)

    if not text or "❌" in text:
        st.error("⚠️ Couldn't extract any valid text.")
    else:
        with st.expander("📝 Raw Extracted Text (first 1000 chars)"):
            st.text(text[:1000])

        parsed = parse_resume_text(text)
        st.subheader("🔍 Parsed Information")

        col1, col2 = st.columns(2)
        with col1:
            for key in ['Name', 'Email', 'Phone']:
                st.write(f"**{key}:** {parsed.get(key, 'Not found')}")
        with col2:
            for key in ['Languages', 'Skills']:
                st.write(f"**{key}:**")
                st.write(parsed.get(key, 'Not found'))

        with st.expander("📚 Education"):
            st.write(parsed.get('Education', 'Not found'))

        with st.expander("💼 Experience"):
            st.write(parsed.get('Experience', 'Not found'))

        # Save outputs
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        with open("outputs/parsed_resume.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=4, ensure_ascii=False)

        # Download buttons
        st.markdown("---")
        st.download_button("📥 Download Parsed JSON", json.dumps(parsed, indent=4, ensure_ascii=False), file_name="parsed_resume.json", mime="application/json")
        st.download_button("📥 Download Raw Text", text, file_name="extracted_text.txt", mime="text/plain")
