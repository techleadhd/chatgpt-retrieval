
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
from lib.config import Config
from lib.db_models import db
from lib.db_models import ExtractedData
from lib.db_models import create_app, db, store_data, query_data
from lib.search import simple_search
from flask import Flask
from lib.config import Config
from lib.db_models import db



from flask import Flask
from lib.db_models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app instance
    db.init_app(app)

    return app







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












