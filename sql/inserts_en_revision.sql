













-- INSERT INTO transaccion_encomienda (
--     num_serie,
--     masivo,
--     descripcion,
--     monto_total,
--     recojo_casa,
--     id_sucursal_origen,
--     fecha,
--     hora,
--     direccion_recojo,
--     clienteid,
--     tipo_comprobanteid
-- ) VALUES (
--     12345,
--     0,
--     'Descripción del envío',
--     150.75,
--     0,
--     10,
--     '2025-05-28',
--     '14:30:00',
--     'Calle Falsa 123',
--     1,
--     2
-- );
-- INSERT INTO paquete (
--     tracking, clave, valor, peso, alto, largo, precio_ruta, ancho, descripcion,
--     direccion_destinatario, telefono_destinatario, num_documento_destinatario,
--     sucursal_destino_id, tipo_documento_destinatario_id, contenido_paqueteid,
--     tipo_recepcionid, salidaid, transaccion_encomienda_num_serie,
--     tipo_empaqueid
-- ) VALUES
-- (1001, 'A123', 120.50, 2.5, 10.0, 20.0, 15.00, 5.0, 'Documentos importantes',
--  'Av. Siempre Viva 742', '987654321', '72428857',
--  1, 1, 2,
--  1, NULL, 12345,
--  1),

-- (1002, 'B456', 300.00, 7.2, 30.0, 40.0, 35.00, 25.0, 'Equipos electrónicos',
--  'Calle Falsa 123', '912345678', '87654321',
--  2, 2, 1,
--  2, NULL, 12345,
--  2);

-- INSERT INTO salida (
--    fecha, hora, recojo, entrega, estado, unidadid
-- ) VALUES
-- ('2025-05-28', '08:30:00', 0, 1, 'P', 1),
-- ('2025-05-28', '09:00:00', 0, 1, 'T', 2),
-- ('2025-05-27', '10:15:00', 0, 1, 'P', 3);

-- INSERT INTO reclamo (
--   nombres_razon, direccion, correo, telefono, n_documento, monto_indemnizado,
--   titulo_incidencia, bien_contratado, monto_reclamado, relacion, fecha_recojo,
--   sucursal_id, descripcion, pedido, causa_reclamoid, tipo_indemnizacionid,
--   paquetetracking, ubigeocodigo, tipo_documentoid, estado_reclamoid
-- ) VALUES (
--   'Carlos Pérez', 'Av. Siempre Viva 123', 'carlos@example.com', '987654321', '12345678', 50.00,
--   'Demora en entrega', 'S', 100.00, 'Q', '2025-05-29',
--   1, 'El servicio fue lento.', 'Requiero reembolso.', 1, 1,
--   2, '100101', 1, 1
-- );





INSERT INTO `transaccion_encomienda` (`num_serie`, `masivo`, `descripcion`, `monto_total`, `recojo_casa`, `id_sucursal_origen`, `fecha`, `hora`, `direccion_recojo`, `comprobante_serie`, `clienteid`, `tipo_comprobanteid`) VALUES
('000001', 0, 'Envío individual #F001-000001', 25.50, 0, 3, '2025-06-16', '22:04:22', '', 'F001-000001', 6, 1),
('000002', 0, 'Envío individual #F001-000002', 25.50, 0, 3, '2025-06-16', '22:10:07', '', 'F001-000002', 6, 1),
('000003', 0, 'Envío individual #F001-000003', 25.50, 0, 3, '2025-06-17', '00:52:35', '', 'F001-000003', 6, 1);


INSERT INTO `paquete` (`tracking`, `clave`, `valor`, `peso`, `qr_url`, `alto`, `cantidad_folios`, `estado_pago`, `largo`, `precio_ruta`, `ancho`, `descripcion`, `nombres_contacto_destinatario`, `apellidos_razon_destinatario`, `direccion_destinatario`, `telefono_destinatario`, `num_documento_destinatario`, `sucursal_destino_id`, `tipo_documento_destinatario_id`, `tipo_empaqueid`, `contenido_paqueteid`, `tipo_recepcionid`, `salidaid`, `transaccion_encomienda_num_serie`, `modalidad_pagoid`) VALUES
(2, '4123', 80.00, 5.50, 'comprobantes/2/qr.png', 40.00, NULL, 'P', 50.00, 25.50, 30.00, '', 'Juan', 'Pérez', '', '987654321', '12345678', 5, 1, 1, 3, 1, NULL, '000002', 1),
(3, '4123', 80.00, 5.50, 'comprobantes/3/qr.png', 40.00, NULL, 'P', 50.00, 25.50, 30.00, '', 'Juan', 'Pérez', '', '987654321', '12345678', 5, 1, 1, 3, 1, NULL, '000003', 1);


INSERT INTO `seguimiento` (`paquetetracking`, `detalle_estadoid`, `fecha`, `hora`, `tipo_comprobanteid`) VALUES
(2, 1, '2025-06-16', '22:10:07', NULL),
(2, 2, '2025-06-17', '00:16:36', NULL),
(2, 3, '2025-06-17', '00:16:42', NULL),
(2, 4, '2025-06-17', '00:19:50', 2),
(2, 5, '2025-06-17', '00:20:30', NULL),
(2, 6, '2025-06-17', '00:23:16', NULL),
(2, 7, '2025-06-17', '00:23:20', NULL),
(3, 1, '2025-06-17', '00:52:35', NULL),
(3, 2, '2025-06-17', '01:03:08', NULL),
(3, 3, '2025-06-17', '01:09:24', NULL);
