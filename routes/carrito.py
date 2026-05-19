from flask import Blueprint, redirect, url_for, session, flash, request, render_template
from base_datos.conexion import db
from utils.verificar_rol_cliente import solo_cliente

carrito_bp = Blueprint("carrito", __name__)


@carrito_bp.route("/carrito/agregar", methods=["POST"])
@solo_cliente
def agregar():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    id_producto = request.form.get("id_producto")
    cursor = db.cursor()

    # Verificar que existe y tiene stock
    cursor.execute(
        "SELECT id FROM productos WHERE id = %s AND activo = TRUE AND cantidad > 0",
        (id_producto,)
    )
    producto = cursor.fetchone()

    if not producto:
        flash("Producto no disponible o sin stock", "error")
        cursor.close()
        return redirect(url_for("productos.productos"))

    # Si ya está en el carrito sumar 1, si no insertar
    cursor.execute(
        "SELECT id, cantidad FROM carrito WHERE id_usuario = %s AND id_producto = %s",
        (session["id"], id_producto)
    )
    item = cursor.fetchone()

    if item:
        cursor.execute(
            "UPDATE carrito SET cantidad = cantidad + 1 WHERE id = %s",
            (item["id"],)
        )
    else:
        cursor.execute(
            "INSERT INTO carrito (id_usuario, id_producto, cantidad) VALUES (%s, %s, 1)",
            (session["id"], id_producto)
        )

    db.commit()
    cursor.close()

    flash("Producto agregado al carrito", "success")
    return redirect(url_for("productos.productos"))


@carrito_bp.route("/carrito")
@solo_cliente
def carrito():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()

    # Traer items del carrito con datos del producto
    cursor.execute("""
        SELECT
            c.id          AS carrito_id,
            c.cantidad    AS cantidad_carrito,
            p.id          AS producto_id,
            p.nombre,
            p.precio,
            p.imagen_url,
            p.cantidad    AS stock
        FROM carrito c
        JOIN productos p ON c.id_producto = p.id
        WHERE c.id_usuario = %s
    """, (session["id"],))

    items = cursor.fetchall()
    cursor.close()

    # Calcular subtotal
    subtotal = sum(item["precio"] * item["cantidad_carrito"] for item in items)

    return render_template("carrito.html", items=items, subtotal=subtotal)


@carrito_bp.route("/carrito/cambiar_cantidad", methods=["POST"])
@solo_cliente
def cambiar_cantidad():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    carrito_id = request.form.get("carrito_id")
    accion     = request.form.get("accion")  # 'sumar' o 'restar'
    cursor     = db.cursor()

    # Traer item y su stock actual
    cursor.execute("""
        SELECT c.id, c.cantidad, p.cantidad AS stock
        FROM carrito c
        JOIN productos p ON c.id_producto = p.id
        WHERE c.id = %s AND c.id_usuario = %s
    """, (carrito_id, session["id"]))
    item = cursor.fetchone()

    if not item:
        cursor.close()
        flash("Item no encontrado", "error")
        return redirect(url_for("carrito.carrito"))

    if accion == "sumar":
        if item["cantidad"] >= item["stock"]:
            flash("No hay más stock disponible", "error")
        else:
            cursor.execute(
                "UPDATE carrito SET cantidad = cantidad + 1 WHERE id = %s",
                (carrito_id,)
            )
            db.commit()

    elif accion == "restar":
        if item["cantidad"] <= 1:
            # Si llega a 0 se elimina
            cursor.execute("DELETE FROM carrito WHERE id = %s", (carrito_id,))
        else:
            cursor.execute(
                "UPDATE carrito SET cantidad = cantidad - 1 WHERE id = %s",
                (carrito_id,)
            )
        db.commit()

    cursor.close()
    return redirect(url_for("carrito.carrito"))


@carrito_bp.route("/carrito/eliminar", methods=["POST"])
@solo_cliente
def eliminar():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    carrito_id = request.form.get("carrito_id")
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM carrito WHERE id = %s AND id_usuario = %s",
        (carrito_id, session["id"])
    )
    db.commit()
    cursor.close()

    flash("Producto eliminado", "error")
    return redirect(url_for("carrito.carrito"))