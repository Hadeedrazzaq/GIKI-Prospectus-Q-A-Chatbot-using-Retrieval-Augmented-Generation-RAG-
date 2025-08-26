# 📁 Data Directory

This directory is where you should place your GIKI-related documents for the chatbot to process.

## 📋 Supported Document Types

- **PDF files** (.pdf) - GIKI Prospectus, Fee Structure, etc.
- **Word documents** (.docx, .doc) - Academic Rules, Student Handbook, etc.
- **Text files** (.txt) - Any plain text documents

## 📂 How to Add Documents

### Option 1: Upload via Web Interface (Recommended)
1. Run the application: `streamlit run app.py`
2. Use the file upload interface in the web app
3. Select your GIKI documents and click "Process Documents"

### Option 2: Place Files in This Directory
You can also place your documents directly in this folder:
- `data/giki_prospectus_2024.pdf`
- `data/fee_structure.pdf`
- `data/academic_rules.docx`
- `data/student_handbook.pdf`
- `data/advisory_handbook.pdf`

## 📚 Recommended Documents

For the best experience, include these GIKI documents:
- UG Prospectus 2024
- Fee Structure
- Academic Rules
- Student Handbook
- Advisory Handbook

## ⚠️ Important Notes

- Maximum file size: 10MB per file
- Maximum 5 documents at a time
- Files are processed and stored in the vector database
- Original files are not stored permanently (only processed content)

## 🔄 Processing

When you upload documents:
1. Text is extracted from the files
2. Content is split into chunks
3. Embeddings are generated for each chunk
4. Chunks are stored in the vector database
5. You can then ask questions about the content

## 🗂️ File Organization

```
data/
├── README.md                 # This file
├── giki_prospectus_2024.pdf  # Example: UG Prospectus
├── fee_structure.pdf         # Example: Fee Structure
├── academic_rules.docx       # Example: Academic Rules
├── student_handbook.pdf      # Example: Student Handbook
└── advisory_handbook.pdf     # Example: Advisory Handbook
```
