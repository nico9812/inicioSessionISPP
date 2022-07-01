from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

views = Blueprint("views", __name__)

@views.route("/")
def index():
    return render_template("home.html", user=current_user)

@views.route("/home")
@login_required
def home():
    flash('Se inicio la sesion!', category='success')
    return render_template("homeAlumno.html")