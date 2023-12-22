import pytest
from your_module import read_file, read_pdf_combined, read_pdf_with_pdfplumber, read_text_file_sync
import os

# Directory where test files are located
TEST_DIR = os.path.join(os.path.dirname(__file__), 'test_files')

@pytest.fixture
def sample_pdf():
    return os.path.join(TEST_DIR, 'makers_brochure.pdf')

@pytest.fixture
def sample_text():
    return os.path.join(TEST_DIR, 'data.txt')

def test_read_file_pdf(sample_pdf):
    content = read_file(sample_pdf)
    assert content is not None
    assert 'expected text in pdf' in content

def test_read_file_text(sample_text):
    content = read_file(sample_text)
    assert content is not None
    assert 'I have been with Makers since 2014' in content

def test_read_pdf_combined(sample_pdf):
    content = read_pdf_combined(sample_pdf)
    assert content is not None
    assert 'Why learn to code with Makers?' in content

def test_read_pdf_with_pdfplumber(sample_pdf):
    content = read_pdf_with_pdfplumber(sample_pdf)
    assert content is not None
    assert 'Why learn to code with Makers?' in content

def test_read_text_file_sync(sample_text):
    content = read_text_file_sync(sample_text)
    assert content is not None
    assert 'I have been with Makers since 2014' in content
