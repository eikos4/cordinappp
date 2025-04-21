from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired # type: ignore

class ProjectForm(FlaskForm):
    name = StringField('Nombre del Proyecto', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    start_date = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Fecha de Fin', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Crear Proyecto')
