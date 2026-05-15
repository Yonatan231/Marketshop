-- Crear la base de datos 
CREATE DATABASE IF NOT EXISTS market_shop_v2;
USE market_shop_v2;

-- Tabla: usuarios
CREATE TABLE usuarios (
    id INT NOT NULL AUTO_INCREMENT,
    correo VARCHAR(100) NOT NULL UNIQUE,
    nombre_completo VARCHAR(100) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL, 
    monedas DECIMAL(10,2) DEFAULT 0.00,
    ultima_vez_monedas DATETIME,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descuento_activo VARCHAR(50) DEFAULT 'ninguno',
    PRIMARY KEY (id)
);

-- Tabla: productos
CREATE TABLE productos (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria ENUM('Zapatos', 'Belleza'),
    imagen_url VARCHAR(500),
    activo BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

-- Tabla: pedidos
CREATE TABLE pedidos (
    id INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    descuento_aplicado INT DEFAULT 0, 
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente', 'pagado', 'enviado', 'entregado') DEFAULT 'pendiente',
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) 
);

-- Tabla: detalle_pedido
CREATE TABLE detalle_pedido (
    id INT NOT NULL AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id) 
);

-- Tabla: carrito
CREATE TABLE carrito (
    id INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id) 
);

