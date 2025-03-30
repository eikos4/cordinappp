from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, SelectField,
    SelectMultipleField, IntegerField, SubmitField, DateTimeLocalField, FileField
)
from wtforms.validators import DataRequired, NumberRange, Email, Optional
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class TaskForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired()])
    description = TextAreaField("Descripción")
    progress = IntegerField("Progreso (%)", validators=[NumberRange(min=0, max=100)])
    status = SelectField("Estado", choices=[
        ("Pendiente", "Pendiente"),
        ("En curso", "En curso"),
        ("Finalizada", "Finalizada")
    ])
    priority = SelectField("Prioridad", choices=[
        ("Baja", "Baja"),
        ("Media", "Media"),
        ("Alta", "Alta")
    ])
    category = SelectField("Categoría", choices=[
        ("Desarrollo", "Desarrollo"),
        ("Investigación", "Investigación"),
        ("Revisión", "Revisión")
    ])
    assigned_to = SelectField("Asignar a usuario", coerce=int)
    dependent_task = SelectField("Tarea Dependiente", coerce=int, validators=[Optional()])
    start_date = DateTimeLocalField("Fecha de Inicio", format='%Y-%m-%dT%H:%M', validators=[Optional()])
    end_date = DateTimeLocalField("Fecha de Finalización", format='%Y-%m-%dT%H:%M', validators=[Optional()])
    attachments = FileField(
            "Adjuntar Archivo",
            validators=[FileAllowed(['jpg', 'xml', 'png', 'gif', 'pdf', 'docx'], "Tipos de archivo permitidos: imágenes, PDF, DOCX.")]
        )

    estimated_time = IntegerField("Tiempo Estimado (en horas)", validators=[Optional()])
    
    comments = TextAreaField("Comentarios")
    submit = SubmitField("Guardar")


class MeetingForm(FlaskForm):
    title = StringField("Título de la reunión", validators=[DataRequired()])
    date = DateTimeLocalField("Fecha y hora", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    created_by_id = SelectField("Responsable", coerce=int, validators=[DataRequired()])
    agenda = TextAreaField("Agenda", validators=[Optional()])
    submit = SubmitField("Guardar")



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")
