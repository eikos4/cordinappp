import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
