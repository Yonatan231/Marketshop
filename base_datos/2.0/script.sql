CREATE DATABASE IF NOT EXISTS market_shop_v2;
USE market_shop_v2;

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

CREATE TABLE productos (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria ENUM('Zapatos', 'Belleza'),
    imagen_url VARCHAR(500),
    activo BOOLEAN DEFAULT TRUE,
    cantidad INT DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE pedidos (
    id INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    descuento_aplicado INT DEFAULT 0, 
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente', 'enviado', 'entregado') DEFAULT 'pendiente',
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) 
);

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

CREATE TABLE carrito (
    id INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id) 
);

INSERT INTO productos (nombre, precio, categoria, imagen_url, cantidad) VALUES
('Sneakers Blancos Dama',        50.00, 'Zapatos', 'sneakers_blancos_dama.png',           10),
('Corrector 00 Snow',            13.00, 'Belleza', 'corrector_00_snow.png',               10),
('Labial Líquido Rojo',           9.00, 'Belleza', 'labial_liquido_rojo.png',             10),
('Locion de Vitamina C',          9.00, 'Belleza', 'locion_de_vitamina_C.png',               10),
('Zapatos Deportivos en Cuero',  90.00, 'Zapatos', 'zapatos_deportivos_en_cuero.png',     10),
('Polvo Suelto Traslucido',          9.00, 'Belleza', 'polvo_suelto_traslucido.png',               10);

