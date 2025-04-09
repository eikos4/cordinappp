# app.py
import os
from flask import Flask
from project import create_app  # Asumiremos que lo definiremos en project/__init__.py

app = create_app()


app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "development")
