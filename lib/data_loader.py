import os
import json
from PyPDF2 import PdfFileReader
import pdfplumber
from data_handler import read_file, read_pdf_combined, read_pdf_with_pdfplumber, read_text_file, read_pdf






# Load data from Scrapy's output (JSON file)
def load_scrapy_data(scrapy_output_file):
    if os.path.exists(scrapy_output_file):
        with open(scrapy_output_file, 'r') as file:
            return json.load(file)
    else:
        return {}

# Combine data from both Scrapy output and text/PDF files
def load_combined_data(data_folder, scrapy_output_file):
    combined_data = load_scrapy_data(scrapy_output_file)

    for file_name in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file_name)
        if file_name.endswith('.pdf'):
            combined_data[file_name] = read_pdf(file_path)
        elif file_name.endswith('.txt'):
            combined_data[file_name] = read_text_file(file_path)

    return combined_data

# Specify the paths
data_folder = '/Users/fawaztarar/Documents/chatgpt/chatgpt-retrieval/data'
scrapy_output_file = '/Users/fawaztarar/Documents/chatgpt/chatgpt-retrieval/myproject/myproject/spiders/output.json'

# Load and combine data
data = load_combined_data(data_folder, scrapy_output_file)




