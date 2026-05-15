from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os
from dotenv import load_dotenv
from routes.iniciar_sesion import iniciar_sesion_bp
from routes.registrarse import registrarse_bp
from models.database import db



load_dotenv()

app = Flask(__name__)

app.register_blueprint(iniciar_sesion_bp)
app.register_blueprint(registrarse_bp)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inventario.html')
def inventario():
     return render_template('index.html')

'''@app.route('/registro.html', methods=['GET', 'POST'] )
def regdgsdfistro():
    

    
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
        return redirect(url_for('login'))

    # Si es GET, mostrar el formulario de registro
    return render_template('registro.html')'''


# -------------------------
# Ejecutar la aplicación
# -------------------------
with app.app_context():
    print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
    products = [
    {
        "id": 1,
        "name": "Labial Mate Premium",
        "price": 25,
        "discount": 10,
        "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=600&q=80",
        "category": "maquillaje",
        "rating": 5,
    },
    {
        "id": 2,
        "name": "Base Líquida Nude",
        "price": 40,
        "discount": 15,
        "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80",
        "category": "maquillaje",
        "rating": 4,
    },
    {
        "id": 3,
        "name": "Sombras de Ojos Palette",
        "price": 35,
        "discount": 20,
        "image": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?auto=format&fit=crop&w=600&q=80",
        "category": "maquillaje",
        "rating": 5,
    },
    {
        "id": 4,
        "name": "Tacones Elegantes",
        "price": 80,
        "discount": 25,
        "image": "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?auto=format&fit=crop&w=600&q=80",
        "category": "zapatos",
        "rating": 4,
    },
    {
        "id": 5,
        "name": "Sneakers Blancos",
        "price": 60,
        "discount": 10,
        "image": "https://images.unsplash.com/photo-1519741498423-1f0f29f2a2d2?auto=format&fit=crop&w=600&q=80",
        "category": "zapatos",
        "rating": 5,
    },
    {
        "id": 6,
        "name": "Botas de Cuero",
        "price": 100,
        "discount": 30,
        "image": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=600&q=80",
        "category": "zapatos",
        "rating": 4,
    },
]

"""@app.route('/')
def home():
    return render_template('index.html', products=products)"""

"""if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)"""
