from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import db

iniciar_sesion_bp = Blueprint("iniciar_sesion", __name__)


@iniciar_sesion_bp.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():

    if request.method == "GET":
        return render_template("iniciar_sesion.html")

    correo = request.form.get("correo", "").strip()
    contrasenia = request.form.get("contrasenia", "").strip()

    if not correo or not contrasenia:
        flash("Debe ingresar correo y contraseña", "error")
        return redirect(url_for("iniciar_sesion.iniciar_sesion"))

    cursor = db.cursor()

    sql = """
        SELECT id, nombre, correo
        FROM usuarios
        WHERE correo = %s AND password = %s
    """

    cursor.execute(sql, (correo, contrasenia))

    usuario = cursor.fetchone()

    cursor.close()

    if usuario is None:
        flash("Correo o contraseña incorrectos", "error")
        return redirect(url_for("iniciar_sesion.iniciar_sesion"))

    session["id"] = usuario["id"]
    session["nombre"]  = usuario["nombre"]
    session["correo"] = usuario["correo"]

    flash("Inicio de sesión exitoso", "success")

    return redirect(url_for("inventario"))