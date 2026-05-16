from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from base_datos.conexion import db
import pymysql  # o mysql.connector, según lo que uses

registro_bp = Blueprint("registro", __name__)

@registro_bp.route('/registro.html', methods=['GET', 'POST'])
def registro():
    
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        correo = request.form['email']
        contrasenia = request.form['contrasenia']

        cursor = db.cursor()

        sql = """
            INSERT INTO usuarios (nombre_completo, correo, contrasenia)
            VALUES (%s, %s, %s)
        """

        try:
            cursor.execute(sql, (nombre_completo, correo, contrasenia))
            db.commit()
            cursor.close()
            return redirect(url_for('sesion.iniciar_sesion'))

        except pymysql.err.IntegrityError:
            db.rollback()
            cursor.close()
            flash("Este correo ya está registrado.", "error")
            return redirect(url_for('registro.registro'))
        
    return render_template('registro.html')