# test_search.py
import pytest
from your_flask_app import simple_search

# Mock data
mock_data = {
    "doc1.txt": "Python is an interpreted, high-level and general-purpose programming language.",
    "doc2.txt": "Python's design philosophy emphasizes code readability with its notable use of significant whitespace."
}

def test_simple_search():
    query = "Python"
    expected_snippet = "general-purpose programming language. Python's design philosophy emphasizes code"
    result = simple_search(query, data=mock_data)
    assert result == expected_snippet

def test_simple_search_no_result():
    query = "nonexistent"
    result = simple_search(query, data=mock_data)
    assert result == "No relevant information found."
