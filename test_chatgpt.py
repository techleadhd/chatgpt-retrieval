import os
import pytest
from chatgpt import read_pdf
from PyPDF2 import PdfReader

def test_read_pdf():
    # Path to a sample PDF file for testing
    sample_pdf_path = os.path.join(os.path.dirname(__file__), 'data/makers_brochure.pdf')

    # Call the function with the sample PDF file
    result = read_pdf(sample_pdf_path)

    # Check that the result is a string (since the function should return the extracted text)
    assert isinstance(result, str)

    # Check that the result is not empty (since the sample PDF file should contain some text)
    assert len(result) > 0



import os
import tempfile
from chatgpt import read_text_file

def test_read_text_file():
    # Create a temporary file and write some text to it
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b'Test text')
        temp_path = temp_file.name

    # Use the function to read the text back from the file
    result = read_text_file(temp_path)

    # Check that the function correctly read the text
    assert result == 'Test text'

    # Clean up the temporary file
    os.remove(temp_path)



import requests
from bs4 import BeautifulSoup
from chatgpt import fetch_website_content

def test_fetch_website_content():
    # Use httpbin to create a test URL that returns a known response
    test_url = 'https://httpbin.org/html'
    expected_text = 'Herman Melville - Moby-Dick'

    # Use the function to fetch and parse the content
    result = fetch_website_content(test_url)

    # Check that the function correctly fetched and parsed the content
    assert expected_text in result





from unittest import mock
from chatgpt import simple_search

def test_simple_search():
    # Mock the data dictionary
    data = {
        'file1.txt': 'This is a test file. It contains some text.',
        'file2.txt': 'This is another test file. It contains some different text.',
    }

    # Patch the data dictionary in the module where simple_search is defined
    with mock.patch('chatgpt.data', data):
        # Test that the function correctly finds the best match for a query
        result = simple_search('test')
        assert 'This is a test file' in result

        # Test that the function returns a message when no match is found
        result = simple_search('nonexistent')
        assert result == 'No relevant information found.'





import json
from unittest import mock
from chatgpt import app

def test_chatbot():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data

@mock.patch('chatgpt.openai.ChatCompletion.create')
@mock.patch('chatgpt.simple_search')
def test_handle_query(mock_simple_search, mock_chat_completion):
    mock_simple_search.return_value = 'Test context'
    mock_chat_completion.return_value = mock.Mock(choices=[mock.Mock(message={'content': 'Test answer'})])

    with app.test_client() as client:
        response = client.post('/query', data=json.dumps({'query': 'Test query'}), content_type='application/json')
        assert response.status_code == 200
        assert b'Test answer' in response.data

        response = client.post('/query', data=json.dumps({}), content_type='application/json')
        assert response.status_code == 400
        assert b'No query provided' in response.data