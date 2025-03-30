from collections import defaultdict
from flask import Blueprint, flash, render_template, request, redirect, url_for, current_app
from flask_login import current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os
from .forms import TaskForm
from .models import db, Task, User, TaskProgressHistory

from datetime import datetime, timedelta
from calendar import monthrange


# Configuración del blueprint
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Carpeta de subida
UPLOAD_FOLDER = os.path.join('project', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'xml', 'jpeg', 'py', 'pdf', 'docx'}

# Función para validar archivos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@tasks_bp.route("/new", methods=["GET", "POST"])
def new_task():
    form = TaskForm()

    # Configurar las opciones dinámicas para los campos del formulario
    users = User.query.all()
    form.assigned_to.choices = [(user.id, user.username) for user in users]

    tasks = Task.query.all()
    form.dependent_task.choices = [(0, "Sin dependencia")] + [(task.id, task.title) for task in tasks]

    if request.method == "POST" and form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            progress=form.progress.data,
            status=form.status.data,
            priority=form.priority.data,
            category=form.category.data,
            assigned_to=form.assigned_to.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            comments=form.comments.data,
            dependent_task_id=form.dependent_task.data if form.dependent_task.data != 0 else None,
            created_by=current_user.id,
            is_active=True
        )

                # Manejar el archivo adjunto
        if form.attachments.data:
            file = form.attachments.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                task.attachment_filename = filename  # Guarda el nombre del archivo
            else:
                flash("Tipo de archivo no permitido. La tarea se guardó sin archivo.", "warning")

        
        # Guardar la tarea
        db.session.add(task)
        db.session.commit()
        flash("Tarea creada exitosamente.", "success")
        return redirect(url_for("tasks.list_tasks"))

    return render_template("tasks/new_task.html", form=form, users=users)

@tasks_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # Obtener la tarea o devolver 404
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)

    # Configurar opciones dinámicas para el formulario
    users = User.query.all()
    form.assigned_to.choices = [(user.id, user.username) for user in users]
    
    tasks = Task.query.filter(Task.id != task_id).all()
    form.dependent_task.choices = [(0, "Sin dependencia")] + [(t.id, t.title) for t in tasks]

    # Preseleccionar los participantes existentes
    selected_participants = [str(p.id) for p in task.participants]

    if request.method == "POST" and form.validate_on_submit():
        # Actualizar los campos de la tarea
        task.title = form.title.data
        task.description = form.description.data

        # Registrar historial de progreso si cambia el valor
        if task.progress != form.progress.data:
            progress_entry = TaskProgressHistory(task=task, progress=form.progress.data)
            db.session.add(progress_entry)

        task.progress = form.progress.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.category = form.category.data
        task.assigned_to = form.assigned_to.data
        task.start_date = form.start_date.data
        task.end_date = form.end_date.data
        task.comments = form.comments.data
        task.dependent_task_id = (
            form.dependent_task.data if form.dependent_task.data != 0 else None
        )

        # Manejar archivo adjunto (opcional)
        if form.attachments.data:
            file = form.attachments.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                task.attachment_filename = filename  # Actualiza el archivo adjunto
            else:
                flash("Tipo de archivo no permitido. Los cambios se han guardado sin actualizar el archivo.", "warning")

        # Actualizar participantes
        task.participants.clear()  # Limpiar los participantes existentes
        selected_participants = request.form.getlist("participants")
        for participant_id in selected_participants:
            user = User.query.get(int(participant_id))
            if user:
                task.participants.append(user)

        # Guardar los cambios en la base de datos
        db.session.commit()
        flash("Tarea actualizada exitosamente.", "success")
        return redirect(url_for("tasks.list_tasks"))

    return render_template(
        "tasks/edit_task.html",
        form=form,
        task=task,
        users=users,
        selected_participants=selected_participants,
    )


@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Tarea eliminada exitosamente.", "info")
    return redirect(url_for("tasks.list_tasks"))


