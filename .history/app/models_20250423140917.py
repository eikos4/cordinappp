from datetime import datetime

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50))
    projects = db.relationship('ProjectUser', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

from app import login
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    progress = db.Column(db.Integer, default=0)
    total_hours = db.Column(db.Float, default=0.0)
    participants = db.relationship('ProjectUser', back_populates='project')
    status = db.Column(db.String(50), default='activo')  # Ej: activo, suspendido, finalizado
    admin_comment = db.Column(db.Text)

class ProjectUser(db.Model):
    __tablename__ = 'project_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    hours_worked = db.Column(db.Float, default=0.0)

    user = db.relationship('User', back_populates='projects')
    project = db.relationship('Project', back_populates='participants')



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    recipient = db.relationship('User', backref='notifications')


class ProjectLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.Text, nullable=False)
    archivo_adjunto = db.Column(db.String(255))  # ruta del archivo subido
    tipo_evento = db.Column(db.String(50), default='comentario')

    # relaciones (opcionales)
    project = db.relationship('Project', backref='logs')
    author = db.relationship('User')



qlalchemy.exc.Error operativo
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no existe la columna: tarea.assigned_to_id [SQL: SELECT tarea.id AS tarea_id, tarea.project_id AS tarea_project_id, tarea.name AS tarea_name, tarea.description AS tarea_description, tarea.estimated_hours AS tarea_estimated_hours, tarea.created_by_id AS tarea_created_by_id, tarea.assigned_to_id AS tarea_assigned_to_id FROM tarea WHERE ? = tarea.project_id] [parámetros: (1,)] (Información sobre este error en: https://sqlalche.me/e/20/e3q8)

Rastreo (última llamada más reciente)
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\sqlalchemy\engine\base.py" , línea 1964 , en_exec_single_context
self.dialecto.hacer_ejecutar(
 ^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\sqlalchemy\engine\default.py" , línea 945 , endo_execute
cursor.execute(declaración, parámetros)
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
La excepción anterior fue la causa directa de la siguiente excepción:
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\app.py" , línea 1536 , en__call__
devolver self.wsgi_app(environ, start_response)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\app.py" , línea 1514 , enwsgi_app
respuesta = self.handle_exception(e)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\app.py" , línea 1511 , enwsgi_app
respuesta = self.full_dispatch_request()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\app.py" , línea 919 , enfull_dispatch_request
rv = self.manejar_excepción_de_usuario(e)
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\app.py" , línea 917 , enfull_dispatch_request
rv = self.solicitud_de_envío()
      ^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\app.py" , línea 902 , endispatch_request
devolver self.asegurar_sincronización(self.funciones_de_vista[regla.punto_final])(**argumentos_de_vista) # tipo: ignorar[sin-ningún-retorno]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask_login\utils.py" , línea 290 , endecorated_view
devuelve current_app.ensure_sync(func)(*args, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\app\routes.py" , línea 62 , endashboard
devuelve render_template('dash_leader.html', proyectos=leader_projects)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\templating.py" , línea 150 , enrender_template
devolver _render(aplicación, plantilla, contexto)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\flask\templating.py" , línea 131 , en_render
rv = plantilla.render(contexto)
      ^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\jinja2\environment.py" , línea 1295 , enrender
self.environment.handle_exception()
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\jinja2\environment.py" , línea 942 , enhandle_exception
generar rewrite_traceback_stack(fuente=fuente)
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\app\templates\dash_leader.html" , línea 1 , entop-level template code
{% extiende 'base.html' %}
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\app\templates\base.html" , línea 205 , entop-level template code
{% block content %}{% endblock %}
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\app\templates\dash_leader.html" , línea 49 , enblock 'content'
{% set tareas = proyecto.tareas %}
Archivo "C:\Users\eikos\OneDrive\Escritorio\ProyectTraker\venv\Lib\site-packages\jinja2\environment.py" , línea 490 , engetattr
devuelve getattr(obj, atributo)
