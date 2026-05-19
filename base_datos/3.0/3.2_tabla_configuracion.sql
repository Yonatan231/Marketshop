CREATE TABLE `configuracion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `valor` text NOT NULL,
  PRIMARY KEY (`id`)
); 

INSERT INTO configuracion (nombre, valor) VALUES
-- Descuentos
('primer_descuento', '10'),
('segundo_descuento', '25'),
('tercer_descuento', '50'),
('cuarto_descuento', '75'),

-- Pedidos
('pedido_minutos_pagado', '2'),
('pedido_minutos_enviado', '5'),
('pedido_minutos_entregado', '10'),
('pedido_valor_envio', '5000'),

-- Recompensas
('recompensa_monedas_checkin', '10'),
('costo_ruleta', '5'),
('recompensa_frecuencia_minutos', '1440');