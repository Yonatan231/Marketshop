from base_datos.conexion import db

def get_configuracion(nombre):
    cursor = db.cursor()
    cursor.execute("SELECT valor FROM configuracion WHERE nombre = %s", (nombre,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado["valor"] if resultado else None

def get_configuracion_int(nombre):
    return int(get_configuracion(nombre))

def get_configuracion_float(nombre):
    return float(get_configuracion(nombre))