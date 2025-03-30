# project/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "at2025status"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///atnote.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configuración de Flask-Login
    login_manager.login_view = 'main.login'  # Redirigir a esta vista si no autenticado
    login_manager.login_message_category = 'info'  # Categoría de mensajes flash

    # Importar modelos para que existan en la BD
    from .models import User, Task, Meeting

    # Necesario para Flask-Login: cargar usuario por ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar los Blueprints
    from .routes import main_bp
    from .tasks import tasks_bp
    from .meetings import meetings_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(meetings_bp)

    return app


