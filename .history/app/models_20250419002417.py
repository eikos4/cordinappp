from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(50))  # admin, leader, participant
    projects = db.relationship('ProjectUser', back_populates='user')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    progress = db.Column(db.Integer, default=0)
    total_hours = db.Column(db.Float, default=0.0)
    participants = db.relationship('ProjectUser', back_populates='project')

class ProjectUser(db.Model):
    __tablename__ = 'project_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    hours_worked = db.Column(db.Float, default=0.0)

    user = db.relationship('User', back_populates='projects')
    project = db.relationship('Project', back_populates='participants')
