"""
Document Processor Utility
"""
from PIL import Image
import io

def process_document(uploaded_file):
    # Simple mock: check file type and size
    file_type = uploaded_file.type
    file_size = uploaded_file.size
    result = {
        "File Type": file_type,
        "File Size": f"{file_size/1024:.2f} KB"
    }
    # If image, try to open and get dimensions
    if file_type.startswith("image"):
        image = Image.open(uploaded_file)
        result["Image Size"] = image.size
        result["Mode"] = image.mode
    # If PDF or DOCX, just show type
    if file_type == "application/pdf":
        result["PDF"] = "PDF file uploaded. (OCR not implemented in demo)"
    if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        result["Word"] = "Word document uploaded. (NLP not implemented in demo)"
    result["Verification"] = "Document processed. (Demo only)"
    return result
