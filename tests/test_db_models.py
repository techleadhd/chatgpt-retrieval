# test_models.py
import pytest
from lib.db_models import create_app, db
from your_flask_app.models import ExtractedData

@pytest.fixture
def test_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_extracted_data_model(test_app):
    with test_app.app_context():
        new_data = ExtractedData(source='test', content='test content')
        db.session.add(new_data)
        db.session.commit()

        assert new_data.id is not None
        assert new_data.source == 'test'
        assert new_data.content == 'test content'


# test_functions.py
import pytest
from your_flask_app import create_app, db, store_data, query_data
from your_flask_app.models import ExtractedData

@pytest.fixture
def test_app():
    # Same as above

def test_store_data(test_app):
    with test_app.app_context():
        store_data('web', 'sample content')
        stored_data = ExtractedData.query.first()
        assert stored_data is not None
        assert stored_data.source == 'web'
        assert stored_data.content == 'sample content'

def test_query_data(test_app):
    with test_app.app_context():
        store_data('web', 'Python is awesome')
        store_data('file', 'Python and Flask')
        results = query_data('Python')
        assert len(results) == 2


