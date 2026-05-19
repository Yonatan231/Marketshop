from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from base_datos.conexion import db
from decimal import Decimal
from base_datos.configuracion import get_configuracion_float

pago_bp = Blueprint("pago", __name__)


def calcular_total(subtotal, descuento_activo):
    COSTO_ENVIO = Decimal(str(get_configuracion_float("pedido_valor_envio")))
    if descuento_activo == "envio_gratis":
        envio = Decimal("0")
        descuento_valor = Decimal("0")

    elif descuento_activo == "ninguno":
        envio = COSTO_ENVIO
        descuento_valor = Decimal("0")

    else:
        try:
            porcentaje = Decimal(descuento_activo)
        except Exception:
            porcentaje = Decimal("0")

        envio = COSTO_ENVIO
        descuento_valor = (subtotal + envio) * (porcentaje / Decimal("100"))

    total = subtotal + envio - descuento_valor
    return envio, descuento_valor, total


@pago_bp.route("/pago")
def pago():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()

    cursor.execute("""
        SELECT
            c.cantidad    AS cantidad_carrito,
            p.nombre,
            p.precio,
            p.cantidad    AS stock
        FROM carrito c
        JOIN productos p ON c.id_producto = p.id
        WHERE c.id_usuario = %s
    """, (session["id"],))
    items = cursor.fetchall()

    if not items:
        flash("Tu carrito está vacío", "error")
        cursor.close()
        return redirect(url_for("carrito.carrito"))

    sin_stock = [i for i in items if i["cantidad_carrito"] > i["stock"]]
    if sin_stock:
        flash("Algunos productos ya no tienen stock suficiente", "error")
        cursor.close()
        return redirect(url_for("carrito.carrito"))

    cursor.execute(
        "SELECT descuento_activo FROM usuarios WHERE id = %s",
        (session["id"],)
    )
    usuario = cursor.fetchone()
    cursor.close()

    descuento_activo = usuario["descuento_activo"] or "ninguno"
    subtotal = sum(i["precio"] * i["cantidad_carrito"] for i in items)
    envio, descuento_valor, total = calcular_total(subtotal, descuento_activo)

    return render_template("pago.html",
        items            = items,
        subtotal         = subtotal,
        envio            = envio,
        descuento_activo = descuento_activo,
        descuento_valor  = descuento_valor,
        total            = total,
        form_data        = None
    )


@pago_bp.route("/pago/confirmar", methods=["POST"])
def confirmar():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    nombre_tarjeta = request.form.get("nombre_tarjeta", "").strip()
    numero_tarjeta = request.form.get("numero_tarjeta", "").strip()
    expiracion     = request.form.get("expiracion", "").strip()
    cvv            = request.form.get("cvv", "").strip()

    errores = []

    if not nombre_tarjeta:
        errores.append("El nombre en la tarjeta es obligatorio")

    if not numero_tarjeta.isdigit() or len(numero_tarjeta) != 16:
        errores.append("El número de tarjeta debe tener 16 dígitos")

    if not expiracion or len(expiracion) != 5 or expiracion[2] != "/":
        errores.append("La fecha debe tener el formato MM/AA")
    else:
        mes, anio = expiracion.split("/")
        if not mes.isdigit() or not anio.isdigit() or not (1 <= int(mes) <= 12):
            errores.append("Fecha de expiración inválida")

    if not cvv.isdigit() or len(cvv) not in (3, 4):
        errores.append("El CVV debe tener 3 o 4 dígitos")

    if errores:
        for e in errores:
            flash(e, "error")

        cursor = db.cursor()
        cursor.execute("""
            SELECT
                c.cantidad    AS cantidad_carrito,
                p.nombre,
                p.precio,
                p.cantidad    AS stock
            FROM carrito c
            JOIN productos p ON c.id_producto = p.id
            WHERE c.id_usuario = %s
        """, (session["id"],))
        items = cursor.fetchall()

        cursor.execute(
            "SELECT descuento_activo FROM usuarios WHERE id = %s",
            (session["id"],)
        )
        usuario = cursor.fetchone()
        cursor.close()

        descuento_activo = usuario["descuento_activo"] or "ninguno"
        subtotal = sum(i["precio"] * i["cantidad_carrito"] for i in items)
        envio, descuento_valor, total = calcular_total(subtotal, descuento_activo)

        return render_template("pago.html",
            items            = items,
            subtotal         = subtotal,
            envio            = envio,
            descuento_activo = descuento_activo,
            descuento_valor  = descuento_valor,
            total            = total,
            form_data        = request.form
        )

    # Todo válido — procesar pedido
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            c.id_producto,
            c.cantidad    AS cantidad_carrito,
            p.precio,
            p.cantidad    AS stock
        FROM carrito c
        JOIN productos p ON c.id_producto = p.id
        WHERE c.id_usuario = %s
    """, (session["id"],))
    items = cursor.fetchall()

    if not items:
        flash("Tu carrito está vacío", "error")
        cursor.close()
        return redirect(url_for("carrito.carrito"))

    cursor.execute(
        "SELECT descuento_activo FROM usuarios WHERE id = %s",
        (session["id"],)
    )
    usuario = cursor.fetchone()
    descuento_activo = usuario["descuento_activo"] or "ninguno"

    subtotal = sum(i["precio"] * i["cantidad_carrito"] for i in items)
    envio, descuento_valor, total = calcular_total(subtotal, descuento_activo)

    if descuento_activo in ("envio_gratis", "ninguno"):
        descuento_bd = 0
    else:
        descuento_bd = int(descuento_activo)

    cursor.execute("""
        INSERT INTO pedidos (id_usuario, subtotal, descuento_aplicado, total)
        VALUES (%s, %s, %s, %s)
    """, (session["id"], subtotal, descuento_bd, total))

    id_pedido = cursor.lastrowid

    for item in items:
        cursor.execute("""
            INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (id_pedido, item["id_producto"], item["cantidad_carrito"], item["precio"]))

        cursor.execute("""
            UPDATE productos SET cantidad = cantidad - %s WHERE id = %s
        """, (item["cantidad_carrito"], item["id_producto"]))

    cursor.execute("DELETE FROM carrito WHERE id_usuario = %s", (session["id"],))
    cursor.execute(
        "UPDATE usuarios SET descuento_activo = 'ninguno' WHERE id = %s",
        (session["id"],)
    )

    db.commit()
    cursor.close()

    flash(f"¡Pedido #{id_pedido} confirmado! Total pagado: ${total:.2f}", "success")
    return redirect(url_for("pedidos.historial"))