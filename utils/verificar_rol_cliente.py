from functools import wraps
from flask import session, redirect, url_for, flash

def solo_cliente(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if not session.get("id"):
            return redirect(url_for("sesion.iniciar_sesion"))
        if session.get("rol") != "cliente":
            flash("Acceso no permitido", "error")
            return redirect(url_for("inicio"))
        return f(*args, **kwargs)
    return decorador