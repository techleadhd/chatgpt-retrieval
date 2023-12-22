from PyPDF2 import PdfReader
import pdfplumber
import os
import json
from PyPDF2 import PdfFileReader



def read_file(file_path):
    # Determine the file type from the extension
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.pdf':
        return read_pdf_combined(file_path)
    elif file_extension.lower() in ['.txt', '.md', '.html']:  # Add other text file extensions if needed
        return read_text_file_sync(file_path)
    else:
        return "Unsupported file format"

def read_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_combined(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page_text = pdf_reader.getPage(page_num).extractText()
            if page_text:
                text += page_text
            else:
                text = read_pdf_with_pdfplumber(file_path)
                break
    return text

def read_pdf_with_pdfplumber(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def read_text_file_sync(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
