from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import AssignUserForm, LogHoursForm, LoginForm, RegistrationForm, ProjectForm, UpdateProgressForm, UpdateProjectStatusForm
from app.models import Notification, ProjectLog, User, Project, ProjectUser
from app import db


import os
from werkzeug.utils import secure_filename
from flask import current_app
from app.forms import ProjectLogForm
from app.utils import send_notification
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

    @app.route('/dashboard')
    @login_required
    def dashboard():
        role = current_user.role

        if role == 'admin':
            users = User.query.all()
            projects = Project.query.all()
            return render_template('dash_admin.html', users=users, projects=projects)

        elif role == 'leader':
            leader_projects = [pu.project for pu in current_user.projects]
            return render_template('dash_leader.html', projects=leader_projects)

        elif role == 'participant':
            assigned_projects = [pu.project for pu in current_user.projects]
            return render_template('dash_participant.html', projects=assigned_projects)

        else:
            flash("Rol no reconocido")
            return redirect(url_for('logout'))

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

    @app.route('/assign', methods=['GET', 'POST'])
    @login_required
    def assign_user():
        if current_user.role not in ['admin', 'leader']:
            flash("No tienes permisos para asignar usuarios.")
            return redirect(url_for('dashboard'))

        form = AssignUserForm()
        form.user_id.choices = [(u.id, f"{u.name} ({u.role})") for u in User.query.all()]
        form.project_id.choices = [(p.id, p.name) for p in Project.query.all()]

        if form.validate_on_submit():
            existing = ProjectUser.query.filter_by(
                user_id=form.user_id.data, project_id=form.project_id.data
            ).first()
            if existing:
                flash("Este usuario ya está asignado a ese proyecto.")
            else:
                relation = ProjectUser(
                    user_id=form.user_id.data,
                    project_id=form.project_id.data,
                    hours_worked=form.hours_worked.data
                )
                db.session.add(relation)
                db.session.commit()
                flash("Usuario asignado al proyecto con éxito.")
            return redirect(url_for('assign_user'))

        return render_template('assign_user.html', form=form)

    @app.route('/log-hours', methods=['GET', 'POST'])
    @login_required
    def log_hours():
        if current_user.role != 'participant':
            flash("Solo los colaboradores pueden registrar horas.")
            return redirect(url_for('dashboard'))

        form = LogHoursForm()
        user_projects = ProjectUser.query.filter_by(user_id=current_user.id).all()
        form.project_id.choices = [(pu.project.id, pu.project.name) for pu in user_projects]

        if form.validate_on_submit():
            relation = ProjectUser.query.filter_by(
                user_id=current_user.id,
                project_id=form.project_id.data
            ).first()

            if relation:
                relation.hours_worked += form.hours.data
                db.session.commit()
                # Notificar a los líderes del proyecto
                leader_users = [pu.user for pu in relation.project.participants if pu.user.role == 'leader']
                for leader in leader_users:
                    send_notification(leader.id, f"{current_user.name} registró {form.hours.data} horas en el proyecto '{relation.project.name}'")

                flash("Horas registradas correctamente.")
            else:
                flash("No estás asignado a este proyecto.")
            return redirect(url_for('log_hours'))

        return render_template('log_hours.html', form=form)

    @app.route('/leader/project-hours')
    @login_required
    def project_hours_summary():
        if current_user.role != 'leader':
            flash("Acceso restringido.")
            return redirect(url_for('dashboard'))

        leader_projects = [pu.project for pu in current_user.projects]
        summary = []
        for project in leader_projects:
            assignments = ProjectUser.query.filter_by(project_id=project.id).all()
            user_data = [{
                'name': a.user.name,
                'email': a.user.email,
                'hours': a.hours_worked
            } for a in assignments]
            summary.append({
                'project': project,
                'users': user_data
            })

        return render_template('leader_project_hours.html', summary=summary)

    @app.route('/admin/metrics')
    @login_required
    def admin_metrics():
        if current_user.role != 'admin':
            flash("Solo administradores pueden ver este panel.")
            return redirect(url_for('dashboard'))

        users = User.query.all()
        projects = Project.query.all()
        assignments = ProjectUser.query.all()

        user_hours = {}
        for a in assignments:
            if a.user.name not in user_hours:
                user_hours[a.user.name] = 0
            user_hours[a.user.name] += a.hours_worked

        project_hours = {}
        for a in assignments:
            if a.project.name not in project_hours:
                project_hours[a.project.name] = 0
            project_hours[a.project.name] += a.hours_worked

        role_counts = {
            'admin': User.query.filter_by(role='admin').count(),
            'leader': User.query.filter_by(role='leader').count(),
            'participant': User.query.filter_by(role='participant').count()
        }

        return render_template('admin_metrics.html',
                               users=users,
                               projects=projects,
                               user_hours=user_hours,
                               project_hours=project_hours,
                               role_counts=role_counts)

    @app.route('/leader/update-progress', methods=['GET', 'POST'])
    @login_required
    def update_project_progress():
        if current_user.role != 'leader':
            flash("Acceso restringido.")
            return redirect(url_for('dashboard'))

        form = UpdateProgressForm()
        leader_projects = [pu.project for pu in current_user.projects]
        form.project_id.choices = [(p.id, p.name) for p in leader_projects]

        if form.validate_on_submit():
            project = Project.query.get(form.project_id.data)
            if project and project in leader_projects:
                project.progress = form.progress.data
                db.session.commit()
                # Notificar a los administradores
                admin_users = User.query.filter_by(role='admin').all()
                for admin in admin_users:
                    send_notification(admin.id, f"{current_user.name} actualizó el progreso del proyecto '{project.name}' a {form.progress.data}%.")




                flash("Progreso actualizado con éxito.")
                return redirect(url_for('update_project_progress'))
            else:
                flash("Proyecto no válido o sin permiso.")

        return render_template('update_progress.html', form=form)

    @app.route('/profile')
    @login_required
    def user_profile():
        user = current_user
        assigned_projects = [pu.project for pu in user.projects]

        total_hours = sum([pu.hours_worked for pu in user.projects])
        num_projects = len(assigned_projects)

        return render_template('profile.html',
                               user=user,
                               projects=assigned_projects,
                               total_hours=total_hours,
                               num_projects=num_projects)
    

    @app.route('/notificaciones')
    @login_required
    def notificaciones():
        notifications = Notification.query.filter_by(recipient_id=current_user.id).order_by(Notification.timestamp.desc()).all()
        return render_template('notificaciones.html', notifications=notifications)
    
    @app.route('/notificacion/<int:id>/leer', methods=['POST'])
    @login_required
    def marcar_notificacion_leida(id):
        noti = Notification.query.get_or_404(id)
        if noti.recipient_id != current_user.id:
            flash("No tienes permiso para modificar esta notificación.")
            return redirect(url_for('notificaciones'))

        noti.is_read = True
        db.session.commit()
        return redirect(url_for('notificaciones'))

    

    @app.route('/admin/update-status', methods=['GET', 'POST'])
    @login_required
    def update_project_status():
        if current_user.role != 'admin':
            flash("Acceso restringido.")
            return redirect(url_for('dashboard'))

        form = UpdateProjectStatusForm()
        form.project_id.choices = [(p.id, p.name) for p in Project.query.all()]

        if form.validate_on_submit():
            project = Project.query.get(form.project_id.data)
            old_status = project.status  # guardar estado anterior

            project.status = form.status.data
            project.admin_comment = form.admin_comment.data
            db.session.commit()

            # Si cambió el estado, notificar a los usuarios asignados
            if old_status != form.status.data:
                assignments = ProjectUser.query.filter_by(project_id=project.id).all()
                for assignment in assignments:
                    recipient = assignment.user
                    if recipient.id != current_user.id:  # No notificar al propio admin
                        mensaje = f"El proyecto '{project.name}' cambió de estado: '{old_status}' → '{form.status.data}'."
                        send_notification(recipient.id, mensaje)

            flash("Estado del proyecto actualizado.")

            return redirect(url_for('update_project_status'))

        return render_template('update_project_status.html', form=form)
    
    
    @app.route('/bitacora/agregar', methods=['GET', 'POST'])
    @login_required
    def agregar_bitacora():
        form = ProjectLogForm()
        form.project_id.choices = [(p.id, p.name) for p in Project.query.all()]

        if form.validate_on_submit():
            archivo_path = None
            if form.archivo_adjunto.data:
                archivo = form.archivo_adjunto.data
                filename = secure_filename(archivo.filename)
                folder = os.path.join(current_app.root_path, 'static', 'uploads', 'project_logs', str(form.project_id.data))
                os.makedirs(folder, exist_ok=True)
                archivo_path = os.path.join(folder, filename)
                archivo.save(archivo_path)
                archivo_path = f'/static/uploads/project_logs/{form.project_id.data}/{filename}'

            log = ProjectLog(
                project_id=form.project_id.data,
                author_id=current_user.id,
                descripcion=form.descripcion.data,
                archivo_adjunto=archivo_path,
                tipo_evento=form.tipo_evento.data
            )
            db.session.add(log)
            db.session.commit()
            flash('Registro agregado a la bitácora.')
            return redirect(url_for('ver_bitacora', project_id=form.project_id.data))

        return render_template('bitacora_agregar.html', form=form)
    
    from app.utils import build_timeline

    @app.route('/bitacora/<int:project_id>')
    @login_required
    def ver_bitacora(project_id):
        project = Project.query.get_or_404(project_id)

        # Obtener los registros en orden cronológico
        registros = ProjectLog.query.filter_by(project_id=project.id).order_by(ProjectLog.timestamp.asc()).all()

        # Construir la línea de tiempo proporcional
        timeline = build_timeline(registros)

        return render_template('bitacora_ver.html', project=project, registros=registros, timeline=timeline)


    @app.route("/calendar")
    @login_required
    def calendar_view():
        projects = Project.query.all()
        events = []

        for project in projects:
            events.append({
                'title': project.name,
                'start': project.start_date.strftime("%Y-%m-%d"),
                'end': project.end_date.strftime("%Y-%m-%d"),
                'color': '#5c02a2'  # morado corporativo
            })

        return render_template("calendar.html", events=events)
    
    from datetime import datetime
    @app.route('/cronograma')
    @login_required
    def cronograma():
        from datetime import timedelta
        projects = Project.query.order_by(Project.start_date).all()

        if projects:
            min_date = min(p.start_date for p in projects)
            max_date = max(p.end_date for p in projects)
            total_days = max((max_date - min_date).days, 1)

            for p in projects:
                offset_days = (p.start_date - min_date).days
                duration_days = max((p.end_date - p.start_date).days, 1)

                p.days_offset = round(offset_days / total_days * 100, 2)
                p.duration_percent = round(duration_days / total_days * 100, 2)

        return render_template('cronograma.html', projects=projects)
    

    
