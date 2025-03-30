from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla intermedia para participantes en reuniones
meeting_participants = db.Table(
    'meeting_participants',
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# Tabla intermedia para participantes en tareas
task_participants = db.Table(
    'task_participants',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class Task(db.Model):
    """Modelo para tareas dentro del sistema."""
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    progress = db.Column(db.Integer, default=0, nullable=False)  # Progreso entre 0 y 100
    status = db.Column(db.String(20), default="Pendiente", nullable=False)
    priority = db.Column(db.String(20), default="Media", nullable=False)
    category = db.Column(db.String(50), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    estimated_time = db.Column(db.Integer, nullable=True)

    # Relaciones
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=True)
    dependent_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    dependent_task = db.relationship('Task', remote_side=[id], backref='dependent_tasks')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relación con participantes (usuarios asignados)
    participants = db.relationship(
        'User',
        secondary=task_participants,
        backref=db.backref('tasks_assigned', lazy='dynamic')
    )


    # Historial de progreso
    progress_history = db.relationship('TaskProgressHistory', backref='task', lazy=True)
    
    def __repr__(self):
        return f"<Task {self.title}, category={self.category}, progress={self.progress}%, active={self.is_active}>"



class TaskProgressHistory(db.Model):
    """Historial de progreso para una tarea."""
    __tablename__ = 'task_progress_history'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    progress = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<TaskProgressHistory task_id={self.task_id}, progress={self.progress}, timestamp={self.timestamp}>"


class User(db.Model, UserMixin):
    """Modelo para usuarios del sistema."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relaciones
    tasks_created = db.relationship('Task', backref='creator', lazy=True, foreign_keys='Task.created_by')
    tasks_updated = db.relationship('Task', backref='updater', lazy=True, foreign_keys='Task.updated_by')
    meetings_created = db.relationship('Meeting', backref='creator', lazy=True)
    meetings_participated = db.relationship(
        'Meeting',
        secondary=meeting_participants,
        backref=db.backref('users_participating', lazy='dynamic')
    )

    def set_password(self, password):
        """Generar un hash de contraseña segura."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Validar una contraseña ingresada con el hash almacenado."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}, active={self.is_active}>"


class Meeting(db.Model):
    """Modelo para reuniones del sistema."""
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Campos adicionales
    agenda = db.Column(db.Text, nullable=True)
    minutes = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)

    # Relaciones
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    participants = db.relationship(
        'User',
        secondary=meeting_participants,
        backref=db.backref('meetings_joined', lazy='dynamic')
    )
    tasks = db.relationship('Task', backref='meeting', lazy=True)

    def __repr__(self):
        return f"<Meeting {self.title} on {self.date}, active={self.is_active}>"
