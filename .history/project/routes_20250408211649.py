from flask import Blueprint, app, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from datetime import datetime

from project.models import User, Task, Meeting
from project.forms import LoginForm

main_bp = Blueprint("main", __name__)

# Ruta de Login
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))  # Redirige si ya está autenticado

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Has iniciado sesión correctamente.", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Nombre de usuario o contraseña incorrectos.", "danger")
    return render_template('login.html', form=form)

# Ruta de Logout
@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("main.login"))

# Ruta Principal Protegida
@main_bp.route("/")
@login_required
def index():
    # Obtener parámetros de paginación y filtros desde la URL
    meetings_page = request.args.get('meetings_page', 1, type=int)
    tasks_page = request.args.get('tasks_page', 1, type=int)
    assigned_to = request.args.get("assigned_to", type=int)

     
    filter_user = request.args.get("filter_user", type=int)
    filter_status = request.args.get("filter_status", type=str)

    # FILTRAR TAREAS
    task_query = Task.query.order_by(Task.id.desc())
    if filter_user:
        task_query = task_query.filter(Task.participants.any(id=filter_user))
    if filter_status:
        task_query = task_query.filter(Task.status == filter_status)

    tasks_pagination = task_query.paginate(page=tasks_page, per_page=5, error_out=False)
    meetings_pagination = Meeting.query.order_by(Meeting.date.desc()).paginate(page=meetings_page, per_page=5, error_out=False)





    # ========================
    # 1) Paginar tareas completas (para resumen + tabla principal)
    # ========================
    tasks_pagination = Task.query.order_by(desc(Task.id)).paginate(
        page=tasks_page, per_page=5, error_out=False
    )
    tasks_all = tasks_pagination.items

    # ========================
    # 2) Tareas filtradas por responsable (sin paginar)
    # ========================
    query_filtered = Task.query.order_by(desc(Task.id))
    if assigned_to:
        query_filtered = query_filtered.filter(Task.assigned_to == assigned_to)
    tasks_filtered = query_filtered.all()

    # ========================
    # 3) Paginar historial de reuniones
    # ========================
    meetings_pagination = Meeting.query.order_by(desc(Meeting.date)).paginate(
        page=meetings_page, per_page=5, error_out=False
    )
    meetings = meetings_pagination.items

    # ========================
    # 4) Usuarios para filtros y participación
    # ========================
    users = User.query.all()
    participants = User.query.all()

    return render_template(
        "index.html",
        meetings=meetings,
        meetings_pagination=meetings_pagination,
        tasks_all=tasks_all,
        tasks_pagination=tasks_pagination,
        tasks_filtered=tasks_filtered,
        users=users,
        participants=participants,
        selected_user=assigned_to
    )



from datetime import datetime

@app.route("/timeline_month")
def timeline_month():
    # Filtra tasks_all al mes en curso
    # Por ejemplo, mes = 4 (abril) y year = 2025
    year = 2025
    month = 4
    tasks_all = Task.query.filter(
        Task.start_date >= datetime(year, month, 1),
        Task.start_date < datetime(year, month+1, 1) # si month < 12
    ).all()

    return render_template(
        "timeline_month.html",
        tasks_all=tasks_all,
        year=year,
        month=month
    )
