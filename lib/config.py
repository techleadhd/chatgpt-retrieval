import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SQLALCHEMY_DATABASE_URI = 'postgresql:///chatbot_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False