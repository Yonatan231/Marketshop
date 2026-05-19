from flask import Blueprint, render_template, session, redirect, url_for, flash
from base_datos.conexion import db
from datetime import datetime
from base_datos.configuracion import get_configuracion_int
from utils.verificar_rol_cliente import solo_cliente

pedidos_bp = Blueprint("pedidos", __name__)

def actualizar_estado(cursor, pedido_id, fecha_pedido):
    ahora   = datetime.now()
    minutos = (ahora - fecha_pedido).total_seconds() / 60

    t_pagado    = get_configuracion_int("pedido_minutos_pagado")
    t_enviado   = get_configuracion_int("pedido_minutos_enviado")
    t_entregado = get_configuracion_int("pedido_minutos_entregado")

    if minutos < t_pagado:
        estado = "pendiente"
    elif minutos < t_enviado:
        estado = "pagado"
    elif minutos < t_entregado:
        estado = "enviado"
    else:
        estado = "entregado"

    cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (estado, pedido_id))
    return estado


@pedidos_bp.route("/pedidos")
@solo_cliente
def historial():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()
    cursor.execute("""
        SELECT id, subtotal, descuento_aplicado, total, fecha_pedido, estado
        FROM pedidos
        WHERE id_usuario = %s
        ORDER BY fecha_pedido DESC
    """, (session["id"],))
    pedidos = cursor.fetchall()

    for pedido in pedidos:
        cursor.execute("""
            SELECT p.nombre, d.cantidad, d.precio_unitario
            FROM detalle_pedido d
            JOIN productos p ON d.id_producto = p.id
            WHERE d.id_pedido = %s
        """, (pedido["id"],))
        pedido["detalle"] = cursor.fetchall()
        pedido["estado"]  = actualizar_estado(cursor, pedido["id"], pedido["fecha_pedido"])

    db.commit()
    cursor.close()

    return render_template("pedidos.html", pedidos=pedidos)