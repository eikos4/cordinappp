# project/meetings.py
from flask import Blueprint, flash, render_template, request, redirect, url_for
from .forms import MeetingForm
from .models import db, Meeting, User

meetings_bp = Blueprint("meetings", __name__, url_prefix="/meetings")

@meetings_bp.route("/new", methods=["GET", "POST"])
def new_meeting():
    form = MeetingForm()

    # Configurar las opciones dinámicas para el campo 'created_by_id'
    users = User.query.all()
    form.created_by_id.choices = [(user.id, user.username) for user in users]

    if request.method == "POST" and form.validate_on_submit():
        meeting = Meeting(
            title=form.title.data,
            date=form.date.data,
            created_by_id=form.created_by_id.data,
            agenda=form.agenda.data,
        )

        # Manejar participantes
        selected_participants = request.form.getlist('participants')
        for participant_id in selected_participants:
            user = User.query.get(int(participant_id))
            if user:
                meeting.participants.append(user)

        db.session.add(meeting)
        db.session.commit()
        flash("Reunión creada exitosamente.", "success")
        return redirect(url_for("meetings.list_meetings"))

    # Renderizar el formulario
    return render_template("meetings/new_meeting.html", form=form, users=users)




@meetings_bp.route("/", methods=["GET"])
def list_meetings():
    # Obtener las reuniones (por ejemplo, ordenadas por fecha)
    all_meetings = Meeting.query.order_by(Meeting.date).all()
    return render_template("meetings/list_meetings.html", meetings=all_meetings)



@meetings_bp.route("/<int:meeting_id>/delete", methods=["POST"])
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)

    # Limpiar manualmente la relación de participantes
    meeting.participants.clear()
    db.session.commit()  # Confirma los cambios en la tabla intermedia

    # Luego elimina la reunión
    db.session.delete(meeting)
    db.session.commit()
    flash("Reunión eliminada con éxito.", "success")
    return redirect(url_for("meetings.list_meetings"))




@meetings_bp.route("/export", methods=["GET"])
def export_meetings():
    import csv
    from flask import Response

    # Obtener todas las reuniones
    meetings = Meeting.query.all()

    # Crear un archivo CSV en memoria
    def generate():
        data = [["ID", "Título", "Fecha", "Creador", "Agenda"]]
        for meeting in meetings:
            data.append([
                meeting.id,
                meeting.title,
                meeting.date.strftime('%Y-%m-%d %H:%M'),
                meeting.creator.username if meeting.creator else "N/A",
                meeting.agenda or "Sin agenda"
            ])
        for row in data:
            yield ",".join(row) + "\n"

    # Configurar la respuesta con el archivo CSV
    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=meetings.csv"}
    )
@meetings_bp.route("/<int:meeting_id>/edit", methods=["GET", "POST"])
def edit_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    form = MeetingForm(obj=meeting)

    # Cargar los usuarios
    users = User.query.all()
    if not users:
        flash("No hay usuarios disponibles. Por favor, crea usuarios primero.", "warning")
        return redirect(url_for("meetings.list_meetings"))

    # Configurar las opciones dinámicas del formulario
    form.created_by_id.choices = [(user.id, user.username) for user in users]

    # Manejar el formulario al enviar
    if request.method == "POST" and form.validate_on_submit():
        meeting.title = form.title.data
        meeting.date = form.date.data
        meeting.agenda = form.agenda.data
        meeting.created_by_id = form.created_by_id.data

        # Actualizar participantes
        meeting.participants.clear()
        selected_participants = request.form.getlist("participants")
        for participant_id in selected_participants:
            user = User.query.get(int(participant_id))
            if user:
                meeting.participants.append(user)

        db.session.commit()
        flash("Reunión actualizada exitosamente.", "success")
        return redirect(url_for("meetings.list_meetings"))

    # Pasar los participantes seleccionados
    selected_participants = [str(user.id) for user in meeting.participants]
    return render_template(
        "meetings/edit_meeting.html",
        form=form,
        users=users,
        meeting=meeting,
        selected_participants=selected_participants
    )
