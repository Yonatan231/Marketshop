from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from base_datos.conexion import db
from datetime import datetime
import random

recompensas_bp = Blueprint("recompensas", __name__)

PREMIOS = [
    { "label": "Envío Gratis",   "valor": "envio_gratis"}, 
    { "label": "Nada",           "valor": "ninguno"},  
    { "label": "10% Descuento",  "valor": "10"},  
    { "label": "25% Descuento",  "valor": "25"},   
    { "label": "50% Descuento",  "valor": "50"}, 
    { "label": "75% Descuento",  "valor": "75"},        
]


@recompensas_bp.route("/recompensas")
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
    checkin_hecho = (ultima is not None and ultima.date() == hoy) if hasattr(ultima, 'date') else False

    return render_template("recompensas.html",
        monedas          = usuario["monedas"],
        descuento_activo = usuario["descuento_activo"] or "ninguno",
        checkin_hecho    = checkin_hecho,
    )


@recompensas_bp.route("/recompensas/checkin", methods=["POST"])
def checkin():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()
    cursor.execute(
        "SELECT monedas, ultima_vez_monedas FROM usuarios WHERE id = %s",
        (session["id"],)
    )
    usuario = cursor.fetchone()

    hoy             = datetime.now().date()
    ultima          = usuario["ultima_vez_monedas"]
    checkin_hecho   = (ultima is not None and ultima.date() == hoy) if hasattr(ultima, 'date') else False

    if checkin_hecho:
        flash("Ya obtuviste tus monedas hoy, vuelve mañana", "error")
    else:
        cursor.execute("""
            UPDATE usuarios
            SET monedas = monedas + 10, ultima_vez_monedas = %s
            WHERE id = %s
        """, (datetime.now(), session["id"]))
        db.commit()
        flash("¡+10 monedas obtenidas!", "success")

    cursor.close()
    return redirect(url_for("recompensas.recompensas"))


@recompensas_bp.route("/recompensas/girar", methods=["POST"])
def girar():
    if not session.get("id"):
        return redirect(url_for("sesion.iniciar_sesion"))

    cursor = db.cursor()
    cursor.execute(
        "SELECT monedas FROM usuarios WHERE id = %s",
        (session["id"],)
    )
    usuario = cursor.fetchone()

    if usuario["monedas"] < 5:
        if request.headers.get("X-Requested-With") == "fetch":
            return jsonify({ "error": "No tienes suficientes monedas" }), 400
        flash("Necesitas al menos 5 monedas para girar", "error")
        cursor.close()
        return redirect(url_for("recompensas.recompensas"))

    premio_index = random.randint(0, len(PREMIOS) - 1)
    premio       = PREMIOS[premio_index]

    cursor.execute("""
        UPDATE usuarios
        SET monedas = monedas - 5, descuento_activo = %s
        WHERE id = %s
    """, (premio["valor"], session["id"]))
    db.commit()

    cursor.execute("SELECT monedas FROM usuarios WHERE id = %s", (session["id"],))
    monedas_nuevas = cursor.fetchone()["monedas"]
    cursor.close()

    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({
            "premio_index" : premio_index,
            "label"        : premio["label"],
            "monedas"      : int(monedas_nuevas)
        })

    flash(f"¡Obtuviste: {premio['label']}!", "success")
    return redirect(url_for("recompensas.recompensas"))