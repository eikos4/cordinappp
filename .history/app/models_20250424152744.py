from datetime import datetime
from datetime import date
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, DateField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional

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


from datetime import date

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    estimated_hours = db.Column(db.Float)
    
    real_hours = db.Column(db.Float)
    status = db.Column(db.String(20), default='pendiente')  # 👈 AÑADE ESTA LÍNEA

    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])

    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='tasks_created')

    project = db.relationship('Project', backref='tasks')
