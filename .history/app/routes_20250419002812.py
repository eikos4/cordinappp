from flask import render_template
from app import app, db
from app.models import Project

@app.route('/projects')
def show_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)



from flask import render_template, redirect, url_for, flash
from app import app, db
from app.models import Project
from app.forms import ProjectForm

@app.route('/projects/create', methods=['GET', 'POST'])
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Proyecto creado con éxito')
        return redirect(url_for('show_projects'))
    return render_template('create_project.html', form=form)
