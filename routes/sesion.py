from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from base_datos.conexion import db

sesion_bp = Blueprint("sesion", __name__)

@sesion_bp.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():

    if request.method == "GET":
        return render_template("iniciar_sesion.html")

    correo = request.form.get("correo", "").strip()
    contrasenia = request.form.get("contrasenia", "").strip()

    if not correo or not contrasenia:
        flash("Debe ingresar correo y contraseña", "error")
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()

    sql = """
        SELECT id, nombre_completo, correo, rol, estado
        FROM usuarios
        WHERE correo = %s AND contrasenia = %s
    """

    cursor.execute(sql, (correo, contrasenia))

    usuario = cursor.fetchone()

    cursor.close()

    if usuario is None:
        flash("Correo o contraseña incorrectos", "error")
        return redirect(url_for("sesion.iniciar_sesion"))

    if not usuario["estado"]:
        flash("Tu cuenta está desactivada. Contacta al administrador.", "error")
        return redirect(url_for("sesion.iniciar_sesion"))

    session["id"]             = usuario["id"]
    session["correo"]         = usuario["correo"]
    session["nombre_completo"] = usuario["nombre_completo"]
    session["rol"]            = usuario["rol"]
    flash("Inicio de sesión exitoso", "success")

    if usuario["rol"] == "administrador":
        return redirect(url_for("administrador.panel"))
    else:
        return redirect(url_for("productos.productos"))

@sesion_bp.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("inicio"))