from flask import Blueprint, render_template, session, redirect, url_for, flash
from base_datos.conexion import db
from datetime import datetime

pedidos_bp = Blueprint("pedidos", __name__)

def calcular_estado(fecha_pedido):
    """
    Calcula el estado según el tiempo transcurrido desde que se hizo el pedido.
    No se guarda en BD, se calcula al momento de mostrar.
    """
    ahora      = datetime.now()
    minutos    = (ahora - fecha_pedido).total_seconds() / 60

    if minutos < 2:
        return "pendiente"
    elif minutos < 5:
        return "pagado"
    elif minutos < 10:
        return "enviado"
    else:
        return "entregado"


@pedidos_bp.route("/pedidos")
def historial():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()

    # Traer pedidos del usuario, del más reciente al más antiguo
    cursor.execute("""
        SELECT id, subtotal, descuento_aplicado, total, fecha_pedido
        FROM pedidos
        WHERE id_usuario = %s
        ORDER BY fecha_pedido DESC
    """, (session["id"],))

    pedidos = cursor.fetchall()

    # Traer el detalle de cada pedido
    for pedido in pedidos:
        cursor.execute("""
            SELECT
                p.nombre,
                d.cantidad,
                d.precio_unitario
            FROM detalle_pedido d
            JOIN productos p ON d.id_producto = p.id
            WHERE d.id_pedido = %s
        """, (pedido["id"],))

        pedido["detalle"] = cursor.fetchall()
        pedido["estado"]  = calcular_estado(pedido["fecha_pedido"])

    cursor.close()

    return render_template("pedidos.html", pedidos=pedidos)