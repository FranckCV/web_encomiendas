













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




