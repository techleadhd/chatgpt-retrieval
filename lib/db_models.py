from flask_sqlalchemy import SQLAlchemy
from chatgpt import app


db = SQLAlchemy()







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


