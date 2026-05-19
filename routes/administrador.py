from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from base_datos.conexion import db
import os
from werkzeug.utils import secure_filename
from base_datos.configuracion import get_configuracion, get_configuracion_float, get_configuracion_int

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


# CRUD de productos
CARPETA_IMAGENES = os.path.join("static", "imagenes", "productos")
EXTENSIONES_PERMITIDAS = {"jpg", "jpeg", "png", "webp"}

def extension_permitida(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONES_PERMITIDAS


@administrador_bp.route("/administrador/productos")
def productos():
    if administrador_inicio(): return administrador_inicio()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM productos")
    lista = cursor.fetchall()
    cursor.close()
    return render_template("administrador_productos.html", productos=lista)


@administrador_bp.route("/administrador/productos/agregar", methods=["GET", "POST"])
def agregar_producto():
    if administrador_inicio(): return administrador_inicio()

    if request.method == "GET":
        return render_template("editar_producto.html", producto=None)

    nombre    = request.form.get("nombre", "").strip()
    precio    = request.form.get("precio", "").strip()
    categoria = request.form.get("categoria", "").strip()
    cantidad  = request.form.get("cantidad", "0").strip()
    imagen    = request.files.get("imagen")

    if not nombre or not precio or not categoria or not imagen:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for("administrador.agregar_producto"))

    if not extension_permitida(imagen.filename):
        flash("Formato de imagen no permitido (jpg, jpeg, png, webp)", "error")
        return redirect(url_for("administrador.agregar_producto"))

    try:
        precio   = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        flash("Precio y cantidad deben ser números válidos", "error")
        return redirect(url_for("administrador.agregar_producto"))

    if precio <= 0 or cantidad < 0:
        flash("El precio debe ser mayor a 0 y la cantidad no puede ser negativa", "error")
        return redirect(url_for("administrador.agregar_producto"))

    filename = secure_filename(imagen.filename)
    imagen.save(os.path.join(CARPETA_IMAGENES, filename))

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, precio, categoria, imagen_url, cantidad)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, precio, categoria, filename, cantidad))
    db.commit()
    cursor.close()

    flash("Producto agregado", "success")
    return redirect(url_for("administrador.productos"))


@administrador_bp.route("/administrador/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if administrador_inicio(): return administrador_inicio()
    cursor = db.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()
        return render_template("editar_producto.html", producto=producto)

    nombre    = request.form.get("nombre", "").strip()
    precio    = request.form.get("precio", "").strip()
    categoria = request.form.get("categoria", "").strip()
    cantidad  = request.form.get("cantidad", "0").strip()
    imagen    = request.files.get("imagen")

    if imagen and imagen.filename:
        if not extension_permitida(imagen.filename):
            flash("Formato de imagen no permitido", "error")
            return redirect(url_for("administrador.editar_producto", id=id))
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(CARPETA_IMAGENES, filename))
    else:
        cursor.execute("SELECT imagen_url FROM productos WHERE id = %s", (id,))
        filename = cursor.fetchone()["imagen_url"]

    try:
        precio   = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        flash("Precio y cantidad deben ser números válidos", "error")
        return redirect(url_for("administrador.editar_producto", id=id))

    if precio <= 0 or cantidad < 0:
        flash("El precio debe ser mayor a 0 y la cantidad no puede ser negativa", "error")
        return redirect(url_for("administrador.editar_producto", id=id))

    cursor.execute("""
        UPDATE productos SET nombre=%s, precio=%s, categoria=%s, imagen_url=%s, cantidad=%s
        WHERE id = %s
    """, (nombre, precio, categoria, filename, cantidad, id))
    db.commit()
    cursor.close()

    flash("Producto actualizado", "success")
    return redirect(url_for("administrador.productos"))


@administrador_bp.route("/administrador/productos/estado/<int:id>", methods=["POST"])
def cambiar_estado_producto(id):
    if administrador_inicio(): return administrador_inicio()
    nuevo_estado = request.form.get("estado") == "1"
    cursor = db.cursor()
    cursor.execute("UPDATE productos SET activo = %s WHERE id = %s", (nuevo_estado, id))
    db.commit()
    cursor.close()
    flash("Estado actualizado", "success")
    return redirect(url_for("administrador.productos"))

# Configuración de descuentos, recompensas y tiempos de pedidos
@administrador_bp.route("/administrador/configuracion/descuentos", methods=["GET", "POST"])
def configuracion_descuentos():
    if administrador_inicio(): return administrador_inicio()

    if request.method == "POST":
        campos = ["primer_descuento", "segundo_descuento", "tercer_descuento", "cuarto_descuento"]
        for campo in campos:
            valor = request.form.get(campo, "").strip()
            try:
                valor_num = float(valor)
            except ValueError:
                flash(f"{campo} debe ser un número", "error")
                return redirect(url_for("administrador.configuracion_descuentos"))
            if valor_num < 0 or valor_num > 100:
                flash("Los descuentos deben estar entre 0 y 100", "error")
                return redirect(url_for("administrador.configuracion_descuentos"))
            cursor = db.cursor()
            cursor.execute("UPDATE configuracion SET valor = %s WHERE nombre = %s", (valor, campo))
            db.commit()
            cursor.close()
        flash("Descuentos actualizados", "success")
        return redirect(url_for("administrador.configuracion_descuentos"))

    valores = {
        "primer_descuento" : get_configuracion("primer_descuento"),
        "segundo_descuento": get_configuracion("segundo_descuento"),
        "tercer_descuento" : get_configuracion("tercer_descuento"),
        "cuarto_descuento" : get_configuracion("cuarto_descuento"),
    }
    return render_template("configuracion_descuentos.html", valores=valores)


@administrador_bp.route("/administrador/configuracion/pedidos", methods=["GET", "POST"])
def configuracion_pedidos():
    if administrador_inicio(): return administrador_inicio()

    campos = ["pedido_minutos_pagado", "pedido_minutos_enviado", "pedido_minutos_entregado", "pedido_valor_envio"]

    if request.method == "POST":
        for campo in campos:
            valor = request.form.get(campo, "").strip()
            try:
                valor_num = float(valor)
            except ValueError:
                flash(f"{campo} debe ser un número", "error")   
                return redirect(url_for("administrador.configuracion_pedidos"))
            if valor_num < 0:
                flash("Los valores no pueden ser negativos", "error")
                return redirect(url_for("administrador.configuracion_pedidos"))
            cursor = db.cursor()
            cursor.execute("UPDATE configuracion SET valor = %s WHERE nombre = %s", (valor, campo))
            db.commit()
            cursor.close()
        flash("Configuración de pedidos actualizada", "success")
        return redirect(url_for("administrador.configuracion_pedidos"))

    valores = {c: get_configuracion(c) for c in campos}
    return render_template("configuracion_pedidos.html", valores=valores)


@administrador_bp.route("/administrador/configuracion/recompensas", methods=["GET", "POST"])
def configuracion_recompensas():
    if administrador_inicio(): return administrador_inicio()

    campos = ["recompensa_monedas_checkin", "costo_ruleta", "recompensa_frecuencia_minutos"]

    if request.method == "POST":
        for campo in campos:
            valor = request.form.get(campo, "").strip()
            try:
                valor_num = float(valor)
            except ValueError:
                flash(f"{campo} debe ser un número", "error")
                return redirect(url_for("administrador.configuracion_recompensas"))
            if valor_num < 0:
                flash("Los valores no pueden ser negativos", "error")
                return redirect(url_for("administrador.configuracion_recompensas"))
            cursor = db.cursor()
            cursor.execute("UPDATE configuracion SET valor = %s WHERE nombre = %s", (valor, campo))
            db.commit()
            cursor.close()
        flash("Configuración de recompensas actualizada", "success")
        return redirect(url_for("administrador.configuracion_recompensas"))

    valores = {c: get_configuracion(c) for c in campos}
    return render_template("configuracion_recompensas.html", valores=valores)