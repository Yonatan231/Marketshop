from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.database import db

registrarse_bp = Blueprint("registrarse", __name__)

@registrarse_bp.route('/registro.html', methods=['GET', 'POST'] )
def registro():
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        correo = request.form['email']
        password = request.form['password']
        
        # Crear cursor
        cursor = db.cursor()

        # Insertar usuario en MySQL
        sql = """
            INSERT INTO usuarios (nombre, correo, password)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (nombre, correo, password))

        # Guardar cambios
        db.commit()

        # Cerrar cursor
        cursor.close()

        # Aquí puedes guardar los datos en una base de datos
        print("Nuevo usuario registrado:")
        print("Nombre:", nombre)
        print("Correo:", correo)
        print("Contraseña:", password)

        # Redirigir al login después del registro
        return redirect(url_for('iniciar_sesion.iniciar_sesion'))
        # Si es GET, mostrar el formulario de registro
        
    return render_template('registro.html')
