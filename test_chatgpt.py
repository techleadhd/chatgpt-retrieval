


import json
import pytest
from chatgpt import app

@pytest.fixture
def client():
    app = create_app()  # Adjust this to how your Flask app is initialized
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_chatbot_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type

def test_query_route(client):
    # Test with valid query
    response = client.post('/query', json={'query': 'Hello'})
    assert response.status_code == 200
    assert 'application/json' in response.content_type
    assert 'answer' in response.get_json()

    # Test with no query
    response = client.post('/query', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_error_route(client):
    response = client.get('/test_error')
    assert response.status_code == 500






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



from unittest import mock
from flask import current_app
from chatgpt import app

def test_handle_exception():
    with app.app_context():
        with app.test_client() as client:
            with mock.patch.object(current_app.logger, 'error') as mock_error:
                response = client.get('/test_error')
                assert response.status_code == 500
                assert b'Internal Server Error' in response.data
                print(mock_error.call_args)