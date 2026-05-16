from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from base_datos.conexion import db

registro_bp = Blueprint("registro", __name__)

@registro_bp.route('/registro.html', methods=['GET', 'POST'] )
def registro():
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_completo = request.form['nombre_completo']
        correo = request.form['email']
        contrasenia = request.form['contrasenia']

        cursor = db.cursor()

        sql = """
            INSERT INTO usuarios (nombre_completo, correo, contrasenia)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (nombre_completo, correo, contrasenia))

        db.commit()

        cursor.close()

        print("Nuevo usuario registrado:")
        print("Nombre:", nombre_completo)
        print("Correo:", correo)
        print("Contraseña:", contrasenia)

        return redirect(url_for('sesion.iniciar_sesion'))
        
    return render_template('registro.html')
