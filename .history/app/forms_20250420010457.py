from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    name = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), EqualTo('password')
    ])
    role = SelectField('Rol', choices=[('admin', 'Administrador'), ('leader', 'Líder'), ('participant', 'Colaborador')])
    submit = SubmitField('Registrarse')

class ProjectForm(FlaskForm):
    name = StringField('Nombre del Proyecto', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    start_date = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fecha de Fin', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Crear Proyecto')



from wtforms import SelectField, FloatField

class AssignUserForm(FlaskForm):
    user_id = SelectField('Usuario', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Proyecto', coerce=int, validators=[DataRequired()])
    hours_worked = FloatField('Horas iniciales (opcional)', default=0.0)
    submit = SubmitField('Asignar')

class LogHoursForm(FlaskForm):
    project_id = SelectField('Proyecto', coerce=int, validators=[DataRequired()])
    hours = FloatField('Horas trabajadas', validators=[DataRequired()])
    submit = SubmitField('Registrar')



from wtforms import IntegerField

class UpdateProgressForm(FlaskForm):
    project_id = SelectField('Proyecto', coerce=int, validators=[DataRequired()])
    progress = IntegerField('Progreso (%)', validators=[DataRequired()])
    submit = SubmitField('Actualizar Progreso')



from wtforms import SelectField, TextAreaField

class UpdateProjectStatusForm(FlaskForm):
    project_id = SelectField('Proyecto', coerce=int, validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('finalizado', 'Finalizado'),
        ('en espera', 'En espera')
    ])
    admin_comment = TextAreaField('Comentario del Administrador')
    submit = SubmitField('Actualizar Estado')



