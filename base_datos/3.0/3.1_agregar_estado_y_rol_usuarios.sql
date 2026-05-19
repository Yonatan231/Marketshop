-- agregar columna rol a usuarios
ALTER TABLE usuarios
ADD COLUMN rol ENUM('cliente', 'administrador') DEFAULT 'cliente';

-- actualizar los usuarios existentes para asignarles el rol de cliente
Update usuarios 
SET rol = 'cliente';

-- agregar un usuario administrador 
INSERT INTO usuarios (nombre_completo, correo, contrasenia, rol) VALUES
('Administrador', 'administrador@gmail.com', '12345', 'administrador');

-- agregar columna estado a usuarios
ALTER TABLE usuarios
ADD COLUMN estado BOOLEAN DEFAULT TRUE;

-- actualizar los usuarios existentes para asignarles estado activo
Update usuarios 
SET estado = TRUE;