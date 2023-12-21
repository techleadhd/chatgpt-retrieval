
import os
import openai

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to read PDF files
from PyPDF2 import PdfReader

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

# Function to read text files
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to fetch and parse website content
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(soup.stripped_strings)
        return text
    except requests.RequestException as e:
        return f"Error fetching website content: {e}"

# Load and index data
data_folder = '/Users/fawaztarar/Documents/chatgpt/chatgpt-retrieval/data'  # Replace with your actual data folder path
data = {}
for file_name in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file_name)
    if file_name.endswith('.pdf'):
        data[file_name] = read_pdf(file_path)
    elif file_name.endswith('.txt'):
        data[file_name] = read_text_file(file_path)

# Fetch and add website content to data
website_content = fetch_website_content('https://makers.tech')
if website_content and not isinstance(website_content, Exception):
    data['makers_tech_website'] = website_content

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

if __name__ == '__main__':
    app.run(debug=False, port=5001) # Set to False in production






























# import os
# import sys
# from flask import Flask, request, jsonify, render_template

# import openai
# from langchain.chains import ConversationalRetrievalChain, RetrievalQA
# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import DirectoryLoader, TextLoader
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.indexes import VectorstoreIndexCreator
# from langchain.indexes.vectorstore import VectorStoreIndexWrapper
# from langchain.llms import OpenAI
# from langchain.vectorstores import Chroma

# import constants

# os.environ["OPENAI_API_KEY"] = constants.APIKEY

# # Enable to save to disk & reuse the model (for repeated queries on the same data)
# PERSIST = False

# # Flask app
# app = Flask(__name__)

# @app.route('/')
# def chatbot():
#     return render_template('ai_chatbot.html')

# # Initialize the ConversationalRetrievalChain
# if PERSIST and os.path.exists("persist"):
#     print("Reusing index...\n")
#     vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
#     index = VectorStoreIndexWrapper(vectorstore=vectorstore)
# else:
#     #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
#     loader = DirectoryLoader("data/")
#     if PERSIST:
#         index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
#     else:
#         index = VectorstoreIndexCreator().from_loaders([loader])

# chain = ConversationalRetrievalChain.from_llm(
#     llm=ChatOpenAI(model="gpt-3.5-turbo"),
#     retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
# )

# @app.route('/query', methods=['POST'])
# def handle_query():
#     data = request.json
#     query = data.get('query')
#     chat_history = data.get('chat_history', [])
    
#     if query:
#         result = chain({"question": query, "chat_history": chat_history})
#         answer = result['answer']
#         chat_history.append((query, answer))
#         return jsonify({"answer": answer, "chat_history": chat_history})
#     else:
#         return jsonify({"error": "No query provided"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)


    #host="0.0.0.0" # Listen for connections _to_ any server
    
