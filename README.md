# Market Shop — MFMS

Aplicación web de e-commerce para maquillaje y zapatos, construida con Python y Flask.

## Características

- Pantalla de inicio con acceso a registro e inicio de sesión.
- Catálogo de productos disponibles.
- Carrito de compras con simulación de pago con tarjeta.
- Historial de pedidos con estados simulados (el estado cambia automáticamente con el tiempo), ordenados del más reciente al más antiguo.
- Recompensas gamificadas: check-in cada x tiempo y ruleta de premios.
- Activar/desactivar cuentas.
- Los valores (descuentos, tiempo en cambiar a x estado, costo de la ruleta, valor envio, frecuencia del chec-in y numero de monedas dadas en cada check-in) se pueden modificar con el rol administrador.
- CRUD de productos.

## Tecnologías

- Backend: Python 3, Flask 
- Frontend: HTML, CSS, JavaScript 
- Base de datos: MySQL 

## Estructura del proyecto

```text
Marketshop/
├── base_datos/
│   ├── 2.0, 3.0...          # Versiones y cambios de la base de datos
│   ├── conexion.py          # Conexión a la base de datos
│   └── configuracion.py     # Archivo que permite obtener los valores de configuración almacenados en la base de datos
├── routes/                  # Un archivo por sección (Blueprints)
├── static/
│   └── imagenes/            
│       └── productos/       # Imágenes de los productos
│       └── sistema/         # Imágenes de generales (fondos, logo..)
├── templates/
│   ├── base.html            # Plantilla base
│   └── *.html               # Vistas de cada sección
├── .env                     # Variables de entorno (no se sube al repo)
├── utils                    # Funciones reutilizables
├── app.py                   # Punto de entrada, configuración de Flask
└── requirements.txt         # Dependencias
```

## Cómo ejecutar

### 1. Crear la base de datos

Abre tu gestor de base de datos (por ejemplo, phpMyAdmin desde XAMPP), copia el contenido de `base_datos/script.sql` y ejecútalo.

### 2. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Base de datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=market_shop_v2

# Sesiones
SECRET_KEY="v8#Lm2@Qx7!Np4$Kr9&Wz5"
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación

```bash
python app.py
```

### 5. Abrir en el navegador

```bash
http://127.0.0.1:5000
```
