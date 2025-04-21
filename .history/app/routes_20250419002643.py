from flask import render_template
from app import app, db
from app.models import Project

@app.route('/projects')
def show_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)
