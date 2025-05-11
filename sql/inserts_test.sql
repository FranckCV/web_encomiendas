-- Sucursal en Chiclayo - Central
INSERT INTO sucursal (
  direccion,
  ubigeocodigo,
  horario_l_v,
  horario_s_d,
  latitud,
  longitud,
  teléfono,
  referencia,
  activo
) VALUES (
  'Av. Mariscal Castilla 208, Chiclayo',
  '130101',
  '08:00-19:00',
  '09:00-17:00',
  -6.7714,
  -79.8409,
  '074-123456',
  'Frente a la cochera "Puerto del Inka"',
  1
);

-- Sucursal en Chiclayo - Santa Victoria
INSERT INTO sucursal (
  direccion,
  ubigeocodigo,
  horario_l_v,
  horario_s_d,
  latitud,
  longitud,
  teléfono,
  referencia,
  activo
) VALUES (
  'Av. Miguel Grau 675, Urb. Santa Victoria, Chiclayo',
  '130101',
  '09:00-13:00,14:00-18:00',
  '09:00-13:00',
  -6.7730,
  -79.8415,
  '074-654321',
  'A una cuadra de la Av. Balta',
  1
);


-- Sucursal en Pimentel
INSERT INTO sucursal (
  direccion,
  ubigeocodigo,
  horario_l_v,
  horario_s_d,
  latitud,
  longitud,
  teléfono,
  referencia,
  activo
) VALUES (
  'Calle Torres Paz Nro. 224, Interior C, Pimentel',
  '130110',
  '09:00-13:00,14:00-18:00',
  '09:00-13:00',
  -6.8280,
  -79.9300,
  '074-345678',
  'Frente al parque principal de Pimentel',
  1
);

-- Sucursal en Lambayeque
INSERT INTO sucursal (
  direccion,
  ubigeocodigo,
  horario_l_v,
  horario_s_d,
  latitud,
  longitud,
  teléfono,
  referencia,
  activo
) VALUES (
  'Av. Huamachuco Nro. 809, Lambayeque',
  '130301',
  '09:00-14:00,15:00-18:00',
  '09:00-13:00',
  -6.7020,
  -79.9060,
  '074-987654',
  'Frente al parque infantil',
  1
);
-- Insertar valores en la tabla tipo_cargo
INSERT INTO tipo_rol (nombre, activo)
VALUES 
('Gerente', 1),
('Operario', 1);

-- Insertar valores en la tabla tamaño_caja
INSERT INTO tamaño_caja (nombre, activo)
VALUES 
('S', 1),  -- Tamaño pequeño
('M', 1),  -- Tamaño mediano
('L', 1),  -- Tamaño grande
('XL', 1), -- Tamaño extra grande
('XXL', 1); -- Tamaño extra extra grande

-- Insertar valores en la tabla estado_encomienda
-- Insertar valores en la tabla estado_encomienda
INSERT INTO estado_encomienda (nombre, descripcion, activo)
VALUES 
('En origen', 'El paquete ha salido de su punto de origen', 1),
('En tránsito', 'El paquete está en camino a su destino', 1),
('En destino', 'El paquete ha llegado a su destino y está listo para su recogida', 1),
('Entregado', 'El paquete ha sido entregado al destinatario', 1);

-- Insertar valores en la tabla tipo_paquete
INSERT INTO tipo_paquete (nombre, activo)
VALUES 
('Accesorios para fiestas', 1),
('Accesorios electrónicos', 1),
('Artículos de limpieza', 1),
('Artículos publicitarios', 1),
('Bisuteria', 1),
('Caja', 1),
('Tarjetas personales', 1),
('Muebles y decohogar', 1),
('Ferretería y construcción', 1),
('Alimentacion y bebidas', 1),
('Cosmeticos', 1),
('Electrohogar', 1),
('Juguetes', 1),
('Material medico', 1),
('Medicinas', 1),
('Repuestos', 1),
('Ropa y accesorios', 1),
('Valija-documentos', 1),
('Utiles de escritorio', 1),
('Utiles de oficina', 1);
