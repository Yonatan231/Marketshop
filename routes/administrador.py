from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from base_datos.conexion import db

administrador_bp = Blueprint("administrador", __name__)

def administrador_inicio():
    if session.get("rol") != "administrador":
        flash("Acceso no permitido", "error")
        return redirect(url_for("inicio"))

@administrador_bp.route("/administrador")
def panel():
    if administrador_inicio(): return administrador_inicio()
    return render_template("administrador.html")

@administrador_bp.route("/administrador/usuarios")
def usuarios():
    if administrador_inicio(): return administrador_inicio()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, correo, nombre_completo, monedas, ultima_vez_monedas,
                fecha_registro, descuento_activo, rol, estado
        FROM usuarios
    """)
    lista = cursor.fetchall()
    cursor.close()
    return render_template("usuarios.html", usuarios=lista)

@administrador_bp.route("/administrador/usuarios/estado/<int:id>", methods=["POST"])
def cambiar_estado(id):
    if administrador_inicio(): return administrador_inicio()

    if id == session.get("id"):
        flash("No puedes desactivar tu propia cuenta", "error")
        return redirect(url_for("administrador.usuarios"))

    nuevo_estado = request.form.get("estado") == "1"
    cursor = db.cursor()
    cursor.execute("UPDATE usuarios SET estado = %s WHERE id = %s", (nuevo_estado, id))
    db.commit()
    cursor.close()
    flash("Estado actualizado", "success")
    return redirect(url_for("administrador.usuarios"))
