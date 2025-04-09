from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc

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
