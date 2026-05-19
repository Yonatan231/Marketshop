from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from base_datos.conexion import db
from datetime import datetime
import random
from base_datos.configuracion import get_configuracion_int
from base_datos.configuracion import get_configuracion_int, get_configuracion
from utils.verificar_rol_cliente import solo_cliente

recompensas_bp = Blueprint("recompensas", __name__)


@recompensas_bp.route("/recompensas")
@solo_cliente
def recompensas():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()
    cursor.execute(
        "SELECT monedas, ultima_vez_monedas, descuento_activo FROM usuarios WHERE id = %s",
        (session["id"],)
    )
    usuario = cursor.fetchone()
    cursor.close()

    hoy           = datetime.now().date()
    ultima        = usuario["ultima_vez_monedas"]
    frecuencia    = get_configuracion_int("recompensa_frecuencia_minutos")
    checkin_hecho = False
    if ultima is not None:
        minutos_transcurridos = (datetime.now() - ultima).total_seconds() / 60
        checkin_hecho = minutos_transcurridos < frecuencia

    return render_template("recompensas.html",
        monedas          = usuario["monedas"],
        descuento_activo = usuario["descuento_activo"] or "ninguno",
        checkin_hecho    = checkin_hecho,
        costo_ruleta     = get_configuracion_int("costo_ruleta"),
        monedas_checkin  = get_configuracion_int("recompensa_monedas_checkin"),
        descuentos       = {
            "primer_descuento" : get_configuracion("primer_descuento"),
            "segundo_descuento": get_configuracion("segundo_descuento"),
            "tercer_descuento" : get_configuracion("tercer_descuento"),
            "cuarto_descuento" : get_configuracion("cuarto_descuento"),
        }
    )


@recompensas_bp.route("/recompensas/checkin", methods=["POST"])
@solo_cliente
def checkin():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    monedas_checkin = get_configuracion_int("recompensa_monedas_checkin")
    frecuencia      = get_configuracion_int("recompensa_frecuencia_minutos")

    cursor = db.cursor()
    cursor.execute(
        "SELECT monedas, ultima_vez_monedas FROM usuarios WHERE id = %s",
        (session["id"],)
    )
    usuario = cursor.fetchone()
    ultima  = usuario["ultima_vez_monedas"]

    checkin_hecho = False
    if ultima is not None:
        minutos_transcurridos = (datetime.now() - ultima).total_seconds() / 60
        checkin_hecho = minutos_transcurridos < frecuencia

    if checkin_hecho:
        flash("Ya obtuviste tus monedas, vuelve más tarde", "error")
    else:
        cursor.execute("""
            UPDATE usuarios
            SET monedas = monedas + %s, ultima_vez_monedas = %s
            WHERE id = %s
        """, (monedas_checkin, datetime.now(), session["id"]))
        db.commit()
        flash(f"¡+{monedas_checkin} monedas obtenidas!", "success")

    cursor.close()
    return redirect(url_for("recompensas.recompensas"))


@recompensas_bp.route("/recompensas/girar", methods=["POST"])
@solo_cliente
def girar():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    PREMIOS = [
        { "label": "Envío Gratis",   "valor": "envio_gratis"}, 
        { "label": "Nada",           "valor": "ninguno"},  
        { "label": f"{get_configuracion('primer_descuento')}% Descuento",  "valor": get_configuracion("primer_descuento") },  
        { "label": f"{get_configuracion('segundo_descuento')}% Descuento", "valor": get_configuracion("segundo_descuento")},  
        { "label": f"{get_configuracion('tercer_descuento')}% Descuento",  "valor": get_configuracion("tercer_descuento")},   
        { "label": f"{get_configuracion('cuarto_descuento')}% Descuento",  "valor": get_configuracion("cuarto_descuento")},        
    ]

    cursor = db.cursor()
    cursor.execute(
        "SELECT monedas FROM usuarios WHERE id = %s",
        (session["id"],)
    )
    usuario = cursor.fetchone()

    costo_ruleta = get_configuracion_int("costo_ruleta")
    if usuario["monedas"] < costo_ruleta:
        if request.headers.get("X-Requested-With") == "fetch":
            return jsonify({ "error": "No tienes suficientes monedas" }), 400
        flash("Necesitas al menos 5 monedas para girar", "error")
        cursor.close()
        return redirect(url_for("recompensas.recompensas"))

    premio_index = random.randint(0, len(PREMIOS) - 1)
    premio       = PREMIOS[premio_index]

    cursor.execute("""
        UPDATE usuarios SET monedas = monedas - %s, descuento_activo = %s WHERE id = %s
    """, (costo_ruleta, premio["valor"], session["id"]))
    db.commit()

    cursor.execute("SELECT monedas FROM usuarios WHERE id = %s", (session["id"],))
    monedas_nuevas = cursor.fetchone()["monedas"]
    cursor.close()

    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({
            "premio_index" : premio_index,
            "label"        : premio["label"],
            "valor"        : premio["valor"], 
            "monedas"      : int(monedas_nuevas)
        })

    flash(f"¡Obtuviste: {premio['label']}!", "success")
    return redirect(url_for("recompensas.recompensas"))