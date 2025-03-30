# migrate.py
from flask_migrate import upgrade
from app import app
from project import db  # Asegúrate de importar también la instancia de db

with app.app_context():
    upgrade()
    print("Migración completada.")
