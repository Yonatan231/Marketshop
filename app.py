from flask import Flask, render_template
import os
from dotenv import load_dotenv
from routes.sesion import sesion_bp
from routes.registro import registro_bp
from routes.productos import productos_bp
from routes.carrito import carrito_bp
from routes.pago import pago_bp
from routes.pedidos import pedidos_bp
from routes.recompensas import recompensas_bp

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(sesion_bp)
app.register_blueprint(registro_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(pago_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(recompensas_bp)
@app.route('/')
def inicio():
    return render_template('inicio.html')

if __name__ == '__main__':
    app.run(debug=True)


