from flask import app, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm, ProjectForm
from app.models import User, Project, ProjectUser
from app import db

def init_routes(app):

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Credenciales inválidas')
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(name=form.name.data, email=form.email.data, role=form.role.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Usuario registrado con éxito')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    
    @app.route('/projects')
    @login_required
    def show_projects():
        projects = Project.query.all()
        return render_template('projects.html', projects=projects)

    @app.route('/projects/create', methods=['GET', 'POST'])
    @login_required
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
            flash('Proyecto creado exitosamente')
            return redirect(url_for('show_projects'))
        return render_template('create_project.html', form=form)



from flask_login import current_user

    @app.route('/dashboard')
    @login_required
    def dashboard():
        role = current_user.role

        if role == 'admin':
            # Podrías traer métricas globales
            users = User.query.all()
            projects = Project.query.all()
            return render_template('dash_admin.html', users=users, projects=projects)

        elif role == 'leader':
            # Solo proyectos que lidera
            leader_projects = [pu.project for pu in current_user.projects]
            return render_template('dash_leader.html', projects=leader_projects)

        elif role == 'participant':
            # Solo proyectos donde participa
            assigned_projects = [pu.project for pu in current_user.projects]
            return render_template('dash_participant.html', projects=assigned_projects)

        else:
            flash("Rol no reconocido")
            return redirect(url_for('logout'))
