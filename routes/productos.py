from flask import Blueprint, render_template, session, redirect, url_for, flash
from base_datos.conexion import db

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/productos")
def productos():
    if not session.get("id"):
        flash("Debes iniciar sesión", "error")
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()
    cursor.execute("SELECT id, nombre, precio, categoria, imagen_url, cantidad FROM productos WHERE activo = TRUE")
    productos = cursor.fetchall()
    cursor.close()

    return render_template("productos.html", productos=productos)