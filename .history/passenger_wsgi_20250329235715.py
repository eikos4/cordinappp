import sys
import os

# Ajusta esta ruta según la carpeta donde subas el proyecto
sys.path.insert(0, os.path.dirname(__file__))

# Importa tu app usando la factory function
from project import create_app

application = create_app()
