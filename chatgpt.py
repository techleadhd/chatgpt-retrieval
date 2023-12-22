
import os
import openai
import requests
from flask import Flask, request, jsonify, render_template
from flask import current_app
import json
from PyPDF2 import PdfReader
from flask_sqlalchemy import SQLAlchemy
import pdfplumber
from bs4 import BeautifulSoup



app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
#es = Elasticsearch()

## DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///chatbot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class ExtractedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String, nullable=False)  # e.g., 'web' or 'file'
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ExtractedData {self.source}>'

@app.before_first_request
def create_tables():
    db.create_all()

def store_data(source, content):
    new_data = ExtractedData(source=source, content=content)
    db.session.add(new_data)
    db.session.commit()

def query_data(keyword):
    search = f"%{keyword}%"
    results = ExtractedData.query.filter(ExtractedData.content.like(search)).all()
    return results








def read_file(file_path):
    # Determine the file type from the extension
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.pdf':
        return read_pdf_combined(file_path)
    elif file_extension.lower() in ['.txt', '.md', '.html']:  # Add other text file extensions if needed
        return read_text_file_sync(file_path)
    else:
        return "Unsupported file format"

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
            combined_data[file_name] = read_pdf_sync(file_path)
        elif file_name.endswith('.txt'):
            combined_data[file_name] = read_text_file_sync(file_path)

    return combined_data

# Specify the paths
data_folder = '/Users/fawaztarar/Documents/chatgpt/chatgpt-retrieval/data'
scrapy_output_file = '/Users/fawaztarar/Documents/chatgpt/chatgpt-retrieval/myproject/myproject/spiders/output.json'

# Load and combine data
data = load_combined_data(data_folder, scrapy_output_file)

# Flask routes and the rest of your app...






def simple_search(query):
    query = query.lower()
    best_match = None
    highest_count = 0

    for file_name, text in data.items():
        text_lower = text.lower()
        count = text_lower.count(query)
        if count > highest_count:
            highest_count = count
            best_match = text

    if best_match:
        start_index = best_match.lower().find(query)
        end_index = start_index + len(query)
        snippet = best_match[max(0, start_index-30):min(end_index+30, len(best_match))]
        return snippet

    return "No relevant information found."



@app.route('/')
def chatbot():
    return render_template('ai_chatbot.html')

@app.route('/query', methods=['POST'])
def handle_query():
    data_request = request.json
    query = data_request.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    context = simple_search(query)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
                {"role": "assistant", "content": context},
            ]
        )
        answer = response.choices[0].message['content']
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"answer": answer})



@app.route('/test_error')
def test_error():
    raise Exception('Test exception')


if __name__ == '__main__':
    app.run(debug=False, port=5001) # Set to False in production












