INSERT INTO empresa (
    id,
    ruc,
    nombre,
    id_sucursal,
    correo,
    nro_telefono,
    logo,
    color_pri,
    color_sec,
    color_ter,
    porcentaje_recojo,
    igv,
    actual
  )
VALUES (
    1,
    20512528458,
    'New Olva',
    54,
    'info@newolva.com',
    '+123 456 789',
    'logo.png',
    '#1d4c82',
    '#13e2da',
    '#1b98e0',
    5.00,
    18.00,
    1
  );
INSERT INTO `modulo` (
    `id`,
    `nombre`,
    `icono`,
    `key`,
    `color`,
    `activo`,
    img
  )
VALUES (
    1,
    'Administración',
    'fa-solid fa-user-tie',
    'administracion',
    '#1A53FF',
    1,
    'administracion.jpg'
  ),
  (
    2,
    'Logística',
    'fa-solid fa-truck-front',
    'logistica',
    '#00F068',
    1,
    'logistica.jpg'
  ),
  (
    3,
    'Encomiendas',
    'fa-solid fa-box',
    'encomienda',
    '#FF5E1A',
    1,
    'encomienda.jpg'
  ),
  (
    4,
    'Atención al cliente',
    'fa-solid fa-circle-question',
    'atencion',
    '#8232D2',
    1,
    'atencion.jpg'
  ),
  (
    5,
    'Ventas',
    'fa-solid fa-file-invoice-dollar',
    'ventas',
    '#ff0000',
    1,
    'ventas.jpg'
  ),
  (
    6,
    'Seguridad',
    'fa-solid fa-shield-halved',
    'seguridad',
    '#F0B000',
    1,
    'seguridad.jpg'
  ),
  (
    7,
    'Personal',
    'fa-solid fa-briefcase',
    'personal',
    '#00E0F0',
    1,
    'personal.jpg'
  );
INSERT INTO `tipo_pagina` (`id`, `nombre`)
VALUES (1, 'Mantenimientos'),
  (2, 'Funcionalidades'),
  (3, 'Transacciones'),
  (4, 'Reportes');


INSERT INTO `pagina` (`id`, `titulo`, `icono`, `activo`, `key`, `mostrar`, `padrepaginaid`, `tipo_paginaid`, `moduloid`) VALUES
(1, 'tipos de unidades', 'fa-solid fa-truck-plane', 1, 'tipo_unidad', 1, NULL, 1, 1),
(2, 'marcas de unidades', 'fa-solid fa-car-side', 1, 'marca', 1, NULL, 1, 1),
(3, 'modelos de unidades', 'fa-solid fa-cogs', 1, 'modelo', 1, NULL, 1, 1),
(4, 'unidades', 'fa-solid fa-truck-fast', 1, 'unidad', 1, NULL, 1, 1),
(5, 'tipos de empaques para paquetes', 'fa-solid fa-truck-plane', 1, 'tipo_empaque', 1, NULL, 1, 3),
(6, 'tipos de recepción de paquetes', 'fa-solid fa-truck-plane', 1, 'tipo_recepcion', 1, NULL, 1, 3),
(7, 'roles', 'fa-solid fa-user-shield', 1, 'rol', 1, NULL, 1, 7),
(8, 'métodos de pago', 'fa-solid fa-money-bill-wave', 1, 'metodo_pago', 1, NULL, 1, 5),
(9, 'empleados', 'fa-solid fa-address-card', 1, 'empleado', 1, NULL, 1, 7),
(10, 'tipos de clientes', 'fa-solid fa-layer-group', 1, 'tipo_cliente', 1, NULL, 1, 6),
(11, 'usuarios', 'fa-solid fa-user', 1, 'usuario', 1, NULL, 1, 6),
(12, 'clientes', 'fa-solid fa-user', 1, 'cliente', 1, NULL, 1, 6),
(13, 'tipos de documentos', 'fa-solid fa-id-card', 1, 'tipo_documento', 1, NULL, 1, 1),
(14, 'tipos de comprobantes', 'fa-solid fa-file-lines', 1, 'tipo_comprobante', 1, NULL, 1, 1),
(15, 'tipos de indemnización', 'fa-solid fa-hand-holding-dollar', 1, 'tipo_indemnizacion', 1, NULL, 1, 4),
(16, 'estados de reclamos', 'fa-solid fa-circle-exclamation', 1, 'estado_reclamo', 1, NULL, 1, 4),
(17, 'tamaños de cajas', 'fa-solid fa-box-open', 1, 'tamanio_caja', 1, NULL, 1, 5),
(18, 'contenido de paquetes', 'fa-solid fa-box-open', 1, 'contenido_paquete', 1, NULL, 1, 3),
(19, 'articulos para encomiendas', 'fa-solid fa-box-open', 1, 'articulo', 1, NULL, 1, 5),
(20, 'estados de encomiendas', 'fa-solid fa-boxes-packing', 1, 'estado_encomienda', 1, NULL, 1, 3),
(21, 'tipos de roles', 'ri-file-user-fill', 1, 'tipo_rol', 1, NULL, 1, 7),
(22, 'Motivos de reclamo', '', 1, 'motivo_reclamo', 1, NULL, 1, 4),
(23, 'Causas de reclamo', '', 1, 'causa_reclamo', 1, NULL, 1, 4),
(24, 'Tarifas de ruta', 'fa-solid fa-dollar', 1, 'tarifa_ruta', 1, NULL, 1, 1),
(25, 'Sucursales', 'ri-store-3-line', 1, 'sucursal', 1, NULL, 1, 1),
(26, 'tipos de reclamos', 'fa-solid fa-book-open-reader', 1, 'tipo_reclamo', 1, NULL, 1, 4),
(28, 'Administración de páginas', 'ri-file-settings-fill', 1, 'administrar_paginas', 1, NULL, 2, 6),
(29, 'Información de la empresa', 'ri-file-lock-fill', 1, 'informacion_empresa', 1, NULL, 2, 1),
(30, 'Reclamo', 'fa fa-bullhorn', 1, 'reclamo', 1, NULL, 1, 4),
(31, 'Preguntas frecuentes', 'fa-solid fa-circle-question', 1, 'pregunta_frecuente', 1, NULL, 1, 4),
(32, 'Listado de paquetes por estado actual y fecha', 'fa-solid fa-boxes', 1, 'paquete_estado_fecha', 1, NULL, 4, 3),
(33, 'Salidas', 'fa-solid fa-van-shuttle', 1, 'salida', 1, NULL, 3, 2),
(34, 'Programación de encomiendas', 'fa-solid fa-boxes-packing', 1, 'transaccion_encomienda', 1, NULL, 3, 3),
(35, 'Programar nueva salida', 'fas fa-shipping-fast', 1, 'salida_informacion', 1, NULL, 2, 2),
(36, 'Reporte de horarios de sucursales', 'fa-solid fa-clock', 1, 'horarios_sucursal', 1, NULL, 4, 1),
(37, 'Reporte de ingresos por periodo', 'fa-solid fa-coins', 1, 'ingresos_periodo', 1, NULL, 4, 1),
(39, 'Listado de empleados por rol', 'fa-solid fa-user-tie', 1, 'listado_general_empleados_rol', 1, NULL, 4, 7),
(40, 'Reporte de Usuarios', 'fa-solid fa-users', 1, 'reporte_usuarios', 1, NULL, 4, 6),
(41, 'Lista de Artículos Más Vendidos', 'fa-solid fa-boxes-stacked', 1, 'articulos_mas_vendidos', 1, NULL, 4, 5),
(42, 'Reporte de Artículos que Necesitan Reposición', 'fa-solid fa-boxes-stacked', 1, 'articulos_reposicion', 1, NULL, 4, 5),
(43, 'Reporte de ventas por periodo', 'fa-solid fa-sack-dollar', 1, 'ventas_periodo', 1, NULL, 4, 5),
(44, 'Descuentos', 'fa-solid fa-percent', 1, 'descuento', 1, NULL, 1, 5),
(45, 'Descuentos de artículos', 'fa-solid fa-percent', 1, 'descuento_articulo', 1, NULL, 1, 5),
(46, 'detalle de un estado de reclamo', 'fa-solid fa-file', 1, 'detalle_reclamo', 1, NULL, 1, 4),
(47, 'Programación de devoluciones', 'ri-truck-line', 1, 'programacion_devolucion', 1, NULL, 2, 3),
(48, 'Escaneo de qr', 'fa-solid fa-qrcode', 1, 'interfaz_insertar_estado', 0, NULL, 2, 2),
(49, 'Paquetes', 'fa-solid fa-boxes', 1, 'paquete', 1, NULL, 3, 3),
(50, 'Uso de unidades', 'fa-solid fa-truck', 1, 'reporte_uso_unidades', 1, NULL, 4, 1),
(51, 'Reporte de reclamos segun tipo , causa y periodo', 'fa-solid fa-clipboard-list', 1, 'reporte_reclamos_tipo_causa_periodo', 1, NULL, 4, 4),
(52, 'Reporte de viajes realizados por unidad', 'fa-solid fa-truck-fast', 1, 'viajes_por_unidad', 1, NULL, 4, 2),
(53, 'Listado de encomiendas por tipo empaque', 'fa-solid fa-boxes-packing', 1, 'encomiendas_listar', 1, NULL, 4, 3),
(54, 'Seguimiento de paquete', NULL, 1, 'seguimiento', 0, NULL, 3, 3),
(55, 'Permisos de acceso', 'ri-file-lock-fill', 1, 'permiso_rol', 0, NULL, 2, 6),
(56, 'Procesar Pago de Paquete', 'fas fa-credit-card', 1, 'pagar_paquete', 0, NULL, 2, 3),
(57, 'Responder reclamos', 'fa-solid fa-headset', 1, 'vista_responder_reclamos', 1, NULL, 2, 4);


INSERT INTO `tipo_rol` (`id`, `nombre`, `descripcion`, `activo`)
VALUES (1, 'SuperAdministador', 'Dios', 1),
  (
    2,
    'Administrador',
    'Roles relacionados con la administración de la empresa y gestión de usuarios.',
    1
  ),
  (3, 'Empleado general', NULL, 1),
  (
    4,
    'Ventas',
    'Roles enfocados en la venta de productos o servicios, y el seguimiento de ventas.',
    1
  ),
  (
    5,
    'Finanzas',
    'Roles relacionados con la gestión financiera, reembolsos, e informes financieros.',
    1
  ),
  (
    6,
    'Almacén y Encomiendas',
    'Roles encargados de la gestión de artículos y encomiendas dentro de la empresa.',
    1
  ),
  (
    7,
    'Personal',
    'Roles administrativos relacionados con la gestión de empleados y recursos humanos.',
    1
  ),
  (
    9,
    'Logística y Operativos',
    'Roles enfocados en la gestión de unidades y logística de los viajes.',
    1
  ),
  (
    10,
    'Atención al Cliente',
    'Roles encargados de la atención al cliente y la gestión de reclamos e incidencias.',
    1
  );
INSERT INTO `rol` (
    `id`,
    `nombre`,
    `descripcion`,
    `activo`,
    `tipo_rolid`
  )
VALUES (1, 'Superadmin', 'El patrón', 1, 1),
  (
    2,
    'Coordinador logístico',
    'Responsable de gestionar los horarios de unidades, artículos para encomiendas, y reportes de viajes.',
    1,
    9
  ),
  (
    3,
    'Conductor',
    'Encargado de gestionar los horarios de las unidades y reportar los viajes realizados.',
    1,
    9
  ),
  (
    4,
    'Empleado de almacén',
    'Responsable de gestionar los artículos para las encomiendas.',
    1,
    6
  ),
  (
    5,
    'Empleado de atención al cliente',
    'Gestión de encomiendas, devoluciones, seguimiento, y reportes de encomiendas entregadas y pendientes.',
    1,
    10
  ),
  (
    6,
    'Agente de devoluciones',
    'Responsable de gestionar devoluciones de encomiendas no recogidas.',
    1,
    10
  ),
  (
    7,
    'Repartidor',
    'Encargado de reportar encomiendas entregadas y pendientes.',
    1,
    6
  ),
  (
    8,
    'Recepcionista de sucursal',
    'Encargado de gestionar encomiendas en la sucursal.',
    1,
    6
  ),
  (
    9,
    'Encargado de reclamos',
    'Responsable de gestionar incidencias y reclamos, así como reembolsos e indemnizaciones.',
    1,
    10
  ),
  (
    10,
    'Responsable de gestión financiera',
    'Encargado de verificar y autorizar reembolsos e indemnizaciones, además de generar reportes financieros.',
    1,
    5
  ),
  (
    11,
    'Administrador de la empresa',
    'Responsable de gestionar las sucursales, rutas, unidades, y reportes financieros y operativos.',
    1,
    2
  ),
  (
    12,
    'Vendedor',
    'Encargado de la venta de artículos para encomiendas y generación de reportes de ventas.',
    1,
    4
  ),
  (
    13,
    'Administrador de personal',
    'Gestión de los aspectos administrativos de los empleados, horarios y personal.',
    1,
    2
  ),
  (
    14,
    'Administrador de usuarios',
    'Responsable de la gestión de usuarios, inicio de sesión, registro, recuperación de contraseña y reportes.',
    1,
    2
  ),
  (15, 'Gestor de unidades', NULL, 1, 3);
INSERT INTO `ubigeo` (
    `codigo`,
    `departamento`,
    `provincia`,
    `distrito`,
    `activo`
  )
VALUES ('100101', 'ICA', 'ICA', 'ICA', 1),
  ('100102', 'ICA', 'ICA', 'LA TINGUIÑA', 1),
  ('100103', 'ICA', 'ICA', 'LOS AQUIJES', 1),
  ('100104', 'ICA', 'ICA', 'PARCONA', 1),
  ('100105', 'ICA', 'ICA', 'PUEBLO NUEVO', 1),
  ('100106', 'ICA', 'ICA', 'SALAS', 1),
  (
    '100107',
    'ICA',
    'ICA',
    'SAN JOSE DE LOS MOLINOS',
    1
  ),
  ('100108', 'ICA', 'ICA', 'SAN JUAN BAUTISTA', 1),
  ('100109', 'ICA', 'ICA', 'SANTIAGO', 1),
  ('100110', 'ICA', 'ICA', 'SUBTANJALLA', 1),
  ('100111', 'ICA', 'ICA', 'YAUCA DEL ROSARIO', 1),
  ('100112', 'ICA', 'ICA', 'TATE', 1),
  ('100113', 'ICA', 'ICA', 'PACHACUTEC', 1),
  ('100114', 'ICA', 'ICA', 'OCUCAJE', 1),
  ('100201', 'ICA', 'CHINCHA', 'CHINCHA ALTA', 1),
  ('100202', 'ICA', 'CHINCHA', 'CHAVIN', 1),
  ('100203', 'ICA', 'CHINCHA', 'CHINCHA BAJA', 1),
  ('100204', 'ICA', 'CHINCHA', 'EL CARMEN', 1),
  ('100205', 'ICA', 'CHINCHA', 'GROCIO PRADO', 1),
  (
    '100206',
    'ICA',
    'CHINCHA',
    'SAN PEDRO DE HUACARPANA',
    1
  ),
  ('100207', 'ICA', 'CHINCHA', 'SUNAMPE', 1),
  ('100208', 'ICA', 'CHINCHA', 'TAMBO DE MORA', 1),
  ('100209', 'ICA', 'CHINCHA', 'ALTO LARAN', 1),
  ('100210', 'ICA', 'CHINCHA', 'PUEBLO NUEVO', 1),
  (
    '100211',
    'ICA',
    'CHINCHA',
    'SAN JUAN DE YANAC',
    1
  ),
  ('100301', 'ICA', 'NAZCA', 'NAZCA', 1),
  ('100302', 'ICA', 'NAZCA', 'CHANGUILLO', 1),
  ('100303', 'ICA', 'NAZCA', 'EL INGENIO', 1),
  ('100304', 'ICA', 'NAZCA', 'MARCONA', 1),
  ('100305', 'ICA', 'NAZCA', 'VISTA ALEGRE', 1),
  ('100401', 'ICA', 'PISCO', 'PISCO', 1),
  ('100402', 'ICA', 'PISCO', 'HUANCANO', 1),
  ('100403', 'ICA', 'PISCO', 'HUMAY', 1),
  ('100404', 'ICA', 'PISCO', 'INDEPENDENCIA', 1),
  ('100405', 'ICA', 'PISCO', 'PARACAS', 1),
  ('100406', 'ICA', 'PISCO', 'SAN ANDRES', 1),
  ('100407', 'ICA', 'PISCO', 'SAN CLEMENTE', 1),
  ('100408', 'ICA', 'PISCO', 'TUPAC AMARU INCA', 1),
  ('100501', 'ICA', 'PALPA', 'PALPA', 1),
  ('100502', 'ICA', 'PALPA', 'LLIPATA', 1),
  ('100503', 'ICA', 'PALPA', 'RIO GRANDE', 1),
  ('100504', 'ICA', 'PALPA', 'SANTA CRUZ', 1),
  ('100505', 'ICA', 'PALPA', 'TIBILLO', 1),
  (
    '10101',
    'AMAZONAS',
    'CHACHAPOYAS',
    'CHACHAPOYAS',
    1
  ),
  (
    '10102',
    'AMAZONAS',
    'CHACHAPOYAS',
    'ASUNCION',
    1
  ),
  ('10103', 'AMAZONAS', 'CHACHAPOYAS', 'BALSAS', 1),
  ('10104', 'AMAZONAS', 'CHACHAPOYAS', 'CHETO', 1),
  (
    '10105',
    'AMAZONAS',
    'CHACHAPOYAS',
    'CHILIQUIN',
    1
  ),
  (
    '10106',
    'AMAZONAS',
    'CHACHAPOYAS',
    'CHUQUIBAMBA',
    1
  ),
  ('10107', 'AMAZONAS', 'CHACHAPOYAS', 'GRANADA', 1),
  ('10108', 'AMAZONAS', 'CHACHAPOYAS', 'HUANCAS', 1),
  (
    '10109',
    'AMAZONAS',
    'CHACHAPOYAS',
    'LA JALCA',
    1
  ),
  (
    '10110',
    'AMAZONAS',
    'CHACHAPOYAS',
    'LEIMEBAMBA',
    1
  ),
  ('10111', 'AMAZONAS', 'CHACHAPOYAS', 'LEVANTO', 1),
  (
    '10112',
    'AMAZONAS',
    'CHACHAPOYAS',
    'MAGDALENA',
    1
  ),
  (
    '10113',
    'AMAZONAS',
    'CHACHAPOYAS',
    'MARISCAL CASTILLA',
    1
  ),
  (
    '10114',
    'AMAZONAS',
    'CHACHAPOYAS',
    'MOLINOPAMPA',
    1
  ),
  (
    '10115',
    'AMAZONAS',
    'CHACHAPOYAS',
    'MONTEVIDEO',
    1
  ),
  ('10116', 'AMAZONAS', 'CHACHAPOYAS', 'OLLEROS', 1),
  (
    '10117',
    'AMAZONAS',
    'CHACHAPOYAS',
    'QUINJALCA',
    1
  ),
  (
    '10118',
    'AMAZONAS',
    'CHACHAPOYAS',
    'SAN FRANCISCO DE DAGUAS',
    1
  ),
  (
    '10119',
    'AMAZONAS',
    'CHACHAPOYAS',
    'SAN ISIDRO DE MAINO',
    1
  ),
  ('10120', 'AMAZONAS', 'CHACHAPOYAS', 'SOLOCO', 1),
  ('10121', 'AMAZONAS', 'CHACHAPOYAS', 'SONCHE', 1),
  ('10201', 'AMAZONAS', 'BAGUA', 'LA PECA', 1),
  ('10202', 'AMAZONAS', 'BAGUA', 'ARAMANGO', 1),
  ('10203', 'AMAZONAS', 'BAGUA', 'COPALLIN', 1),
  ('10204', 'AMAZONAS', 'BAGUA', 'EL PARCO', 1),
  ('10205', 'AMAZONAS', 'BAGUA', 'BAGUA', 1),
  ('10206', 'AMAZONAS', 'BAGUA', 'IMAZA', 1),
  ('10301', 'AMAZONAS', 'BONGARA', 'JUMBILLA', 1),
  ('10302', 'AMAZONAS', 'BONGARA', 'COROSHA', 1),
  ('10303', 'AMAZONAS', 'BONGARA', 'CUISPES', 1),
  ('10304', 'AMAZONAS', 'BONGARA', 'CHISQUILLA', 1),
  ('10305', 'AMAZONAS', 'BONGARA', 'CHURUJA', 1),
  ('10306', 'AMAZONAS', 'BONGARA', 'FLORIDA', 1),
  ('10307', 'AMAZONAS', 'BONGARA', 'RECTA', 1),
  ('10308', 'AMAZONAS', 'BONGARA', 'SAN CARLOS', 1),
  ('10309', 'AMAZONAS', 'BONGARA', 'SHIPASBAMBA', 1),
  ('10310', 'AMAZONAS', 'BONGARA', 'VALERA', 1),
  (
    '10311',
    'AMAZONAS',
    'BONGARA',
    'YAMBRASBAMBA',
    1
  ),
  ('10312', 'AMAZONAS', 'BONGARA', 'JAZAN', 1),
  ('10401', 'AMAZONAS', 'LUYA', 'LAMUD', 1),
  ('10402', 'AMAZONAS', 'LUYA', 'CAMPORREDONDO', 1),
  ('10403', 'AMAZONAS', 'LUYA', 'COCABAMBA', 1),
  ('10404', 'AMAZONAS', 'LUYA', 'COLCAMAR', 1),
  ('10405', 'AMAZONAS', 'LUYA', 'CONILA', 1),
  ('10406', 'AMAZONAS', 'LUYA', 'INGUILPATA', 1),
  ('10407', 'AMAZONAS', 'LUYA', 'LONGUITA', 1),
  ('10408', 'AMAZONAS', 'LUYA', 'LONYA CHICO', 1),
  ('10409', 'AMAZONAS', 'LUYA', 'LUYA', 1),
  ('10410', 'AMAZONAS', 'LUYA', 'LUYA VIEJO', 1),
  ('10411', 'AMAZONAS', 'LUYA', 'MARIA', 1),
  ('10412', 'AMAZONAS', 'LUYA', 'OCALLI', 1),
  ('10413', 'AMAZONAS', 'LUYA', 'OCUMAL', 1),
  ('10414', 'AMAZONAS', 'LUYA', 'PISUQUIA', 1),
  ('10415', 'AMAZONAS', 'LUYA', 'SAN CRISTOBAL', 1),
  (
    '10416',
    'AMAZONAS',
    'LUYA',
    'SAN FRANCISCO DEL YESO',
    1
  ),
  ('10417', 'AMAZONAS', 'LUYA', 'SAN JERONIMO', 1),
  (
    '10418',
    'AMAZONAS',
    'LUYA',
    'SAN JUAN DE LOPECANCHA',
    1
  ),
  ('10419', 'AMAZONAS', 'LUYA', 'SANTA CATALINA', 1),
  ('10420', 'AMAZONAS', 'LUYA', 'SANTO TOMAS', 1),
  ('10421', 'AMAZONAS', 'LUYA', 'TINGO', 1),
  ('10422', 'AMAZONAS', 'LUYA', 'TRITA', 1),
  ('10423', 'AMAZONAS', 'LUYA', 'PROVIDENCIA', 1),
  (
    '10501',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'SAN NICOLAS',
    1
  ),
  (
    '10502',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'COCHAMAL',
    1
  ),
  (
    '10503',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'CHIRIMOTO',
    1
  ),
  (
    '10504',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'HUAMBO',
    1
  ),
  (
    '10505',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'LIMABAMBA',
    1
  ),
  (
    '10506',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'LONGAR',
    1
  ),
  (
    '10507',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'MILPUC',
    1
  ),
  (
    '10508',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'MARISCAL BENAVIDES',
    1
  ),
  (
    '10509',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'OMIA',
    1
  ),
  (
    '10510',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'SANTA ROSA',
    1
  ),
  (
    '10511',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'TOTORA',
    1
  ),
  (
    '10512',
    'AMAZONAS',
    'RODRIGUEZ DE MENDOZA',
    'VISTA ALEGRE',
    1
  ),
  ('10601', 'AMAZONAS', 'CONDORCANQUI', 'NIEVA', 1),
  (
    '10602',
    'AMAZONAS',
    'CONDORCANQUI',
    'RIO SANTIAGO',
    1
  ),
  (
    '10603',
    'AMAZONAS',
    'CONDORCANQUI',
    'EL CENEPA',
    1
  ),
  (
    '10701',
    'AMAZONAS',
    'UTCUBAMBA',
    'BAGUA GRANDE',
    1
  ),
  ('10702', 'AMAZONAS', 'UTCUBAMBA', 'CAJARURO', 1),
  ('10703', 'AMAZONAS', 'UTCUBAMBA', 'CUMBA', 1),
  (
    '10704',
    'AMAZONAS',
    'UTCUBAMBA',
    'EL MILAGRO',
    1
  ),
  ('10705', 'AMAZONAS', 'UTCUBAMBA', 'JAMALCA', 1),
  (
    '10706',
    'AMAZONAS',
    'UTCUBAMBA',
    'LONYA GRANDE',
    1
  ),
  ('10707', 'AMAZONAS', 'UTCUBAMBA', 'YAMON', 1),
  ('110101', 'JUNIN', 'HUANCAYO', 'HUANCAYO', 1),
  (
    '110103',
    'JUNIN',
    'HUANCAYO',
    'CARHUACALLANGA',
    1
  ),
  ('110104', 'JUNIN', 'HUANCAYO', 'COLCA', 1),
  ('110105', 'JUNIN', 'HUANCAYO', 'CULLHUAS', 1),
  ('110106', 'JUNIN', 'HUANCAYO', 'CHACAPAMPA', 1),
  ('110107', 'JUNIN', 'HUANCAYO', 'CHICCHE', 1),
  ('110108', 'JUNIN', 'HUANCAYO', 'CHILCA', 1),
  ('110109', 'JUNIN', 'HUANCAYO', 'CHONGOS ALTO', 1),
  ('110112', 'JUNIN', 'HUANCAYO', 'CHUPURO', 1),
  ('110113', 'JUNIN', 'HUANCAYO', 'EL TAMBO', 1),
  ('110114', 'JUNIN', 'HUANCAYO', 'HUACRAPUQUIO', 1),
  ('110116', 'JUNIN', 'HUANCAYO', 'HUALHUAS', 1),
  ('110118', 'JUNIN', 'HUANCAYO', 'HUANCAN', 1),
  ('110119', 'JUNIN', 'HUANCAYO', 'HUASICANCHA', 1),
  ('110120', 'JUNIN', 'HUANCAYO', 'HUAYUCACHI', 1),
  ('110121', 'JUNIN', 'HUANCAYO', 'INGENIO', 1),
  ('110122', 'JUNIN', 'HUANCAYO', 'PARIAHUANCA', 1),
  ('110123', 'JUNIN', 'HUANCAYO', 'PILCOMAYO', 1),
  ('110124', 'JUNIN', 'HUANCAYO', 'PUCARA', 1),
  ('110125', 'JUNIN', 'HUANCAYO', 'QUICHUAY', 1),
  ('110126', 'JUNIN', 'HUANCAYO', 'QUILCAS', 1),
  ('110127', 'JUNIN', 'HUANCAYO', 'SAN AGUSTIN', 1),
  (
    '110128',
    'JUNIN',
    'HUANCAYO',
    'SAN JERONIMO DE TUNAN',
    1
  ),
  (
    '110131',
    'JUNIN',
    'HUANCAYO',
    'SANTO DOMINGO DE ACOBAMBA',
    1
  ),
  ('110132', 'JUNIN', 'HUANCAYO', 'SAÑO', 1),
  ('110133', 'JUNIN', 'HUANCAYO', 'SAPALLANGA', 1),
  ('110134', 'JUNIN', 'HUANCAYO', 'SICAYA', 1),
  ('110136', 'JUNIN', 'HUANCAYO', 'VIQUES', 1),
  ('110201', 'JUNIN', 'CONCEPCION', 'CONCEPCION', 1),
  ('110202', 'JUNIN', 'CONCEPCION', 'ACO', 1),
  ('110203', 'JUNIN', 'CONCEPCION', 'ANDAMARCA', 1),
  ('110204', 'JUNIN', 'CONCEPCION', 'COMAS', 1),
  ('110205', 'JUNIN', 'CONCEPCION', 'COCHAS', 1),
  ('110206', 'JUNIN', 'CONCEPCION', 'CHAMBARA', 1),
  (
    '110207',
    'JUNIN',
    'CONCEPCION',
    'HEROINAS TOLEDO',
    1
  ),
  ('110208', 'JUNIN', 'CONCEPCION', 'MANZANARES', 1),
  (
    '110209',
    'JUNIN',
    'CONCEPCION',
    'MARISCAL CASTILLA',
    1
  ),
  ('110210', 'JUNIN', 'CONCEPCION', 'MATAHUASI', 1),
  ('110211', 'JUNIN', 'CONCEPCION', 'MITO', 1),
  (
    '110212',
    'JUNIN',
    'CONCEPCION',
    'NUEVE DE JULIO',
    1
  ),
  ('110213', 'JUNIN', 'CONCEPCION', 'ORCOTUNA', 1),
  (
    '110214',
    'JUNIN',
    'CONCEPCION',
    'SANTA ROSA DE OCOPA',
    1
  ),
  (
    '110215',
    'JUNIN',
    'CONCEPCION',
    'SAN JOSE DE QUERO',
    1
  ),
  ('110301', 'JUNIN', 'JAUJA', 'JAUJA', 1),
  ('110302', 'JUNIN', 'JAUJA', 'ACOLLA', 1),
  ('110303', 'JUNIN', 'JAUJA', 'APATA', 1),
  ('110304', 'JUNIN', 'JAUJA', 'ATAURA', 1),
  ('110305', 'JUNIN', 'JAUJA', 'CANCHAYLLO', 1),
  ('110306', 'JUNIN', 'JAUJA', 'EL MANTARO', 1),
  ('110307', 'JUNIN', 'JAUJA', 'HUAMALI', 1),
  ('110308', 'JUNIN', 'JAUJA', 'HUARIPAMPA', 1),
  ('110309', 'JUNIN', 'JAUJA', 'HUERTAS', 1),
  ('110310', 'JUNIN', 'JAUJA', 'JANJAILLO', 1),
  ('110311', 'JUNIN', 'JAUJA', 'JULCAN', 1),
  ('110312', 'JUNIN', 'JAUJA', 'LEONOR ORDOÑEZ', 1),
  ('110313', 'JUNIN', 'JAUJA', 'LLOCLLAPAMPA', 1),
  ('110314', 'JUNIN', 'JAUJA', 'MARCO', 1),
  ('110315', 'JUNIN', 'JAUJA', 'MASMA', 1),
  ('110316', 'JUNIN', 'JAUJA', 'MOLINOS', 1),
  ('110317', 'JUNIN', 'JAUJA', 'MONOBAMBA', 1),
  ('110318', 'JUNIN', 'JAUJA', 'MUQUI', 1),
  ('110319', 'JUNIN', 'JAUJA', 'MUQUIYAUYO', 1),
  ('110320', 'JUNIN', 'JAUJA', 'PACA', 1),
  ('110321', 'JUNIN', 'JAUJA', 'PACCHA', 1),
  ('110322', 'JUNIN', 'JAUJA', 'PANCAN', 1),
  ('110323', 'JUNIN', 'JAUJA', 'PARCO', 1),
  ('110324', 'JUNIN', 'JAUJA', 'POMACANCHA', 1),
  ('110325', 'JUNIN', 'JAUJA', 'RICRAN', 1),
  ('110326', 'JUNIN', 'JAUJA', 'SAN LORENZO', 1),
  (
    '110327',
    'JUNIN',
    'JAUJA',
    'SAN PEDRO DE CHUNAN',
    1
  ),
  ('110328', 'JUNIN', 'JAUJA', 'SINCOS', 1),
  ('110329', 'JUNIN', 'JAUJA', 'TUNAN MARCA', 1),
  ('110330', 'JUNIN', 'JAUJA', 'YAULI', 1),
  ('110331', 'JUNIN', 'JAUJA', 'CURICACA', 1),
  ('110332', 'JUNIN', 'JAUJA', 'MASMA CHICCHE', 1),
  ('110333', 'JUNIN', 'JAUJA', 'SAUSA', 1),
  ('110334', 'JUNIN', 'JAUJA', 'YAUYOS', 1),
  ('110401', 'JUNIN', 'JUNIN', 'JUNIN', 1),
  ('110402', 'JUNIN', 'JUNIN', 'CARHUAMAYO', 1),
  ('110403', 'JUNIN', 'JUNIN', 'ONDORES', 1),
  ('110404', 'JUNIN', 'JUNIN', 'ULCUMAYO', 1),
  ('110501', 'JUNIN', 'TARMA', 'TARMA', 1),
  ('110502', 'JUNIN', 'TARMA', 'ACOBAMBA', 1),
  ('110503', 'JUNIN', 'TARMA', 'HUARICOLCA', 1),
  ('110504', 'JUNIN', 'TARMA', 'HUASAHUASI', 1),
  ('110505', 'JUNIN', 'TARMA', 'LA UNION', 1),
  ('110506', 'JUNIN', 'TARMA', 'PALCA', 1),
  ('110507', 'JUNIN', 'TARMA', 'PALCAMAYO', 1),
  (
    '110508',
    'JUNIN',
    'TARMA',
    'SAN PEDRO DE CAJAS',
    1
  ),
  ('110509', 'JUNIN', 'TARMA', 'TAPO', 1),
  ('110601', 'JUNIN', 'YAULI', 'LA OROYA', 1),
  ('110602', 'JUNIN', 'YAULI', 'CHACAPALPA', 1),
  ('110603', 'JUNIN', 'YAULI', 'HUAY-HUAY', 1),
  ('110604', 'JUNIN', 'YAULI', 'MARCAPOMACOCHA', 1),
  ('110605', 'JUNIN', 'YAULI', 'MOROCOCHA', 1),
  ('110606', 'JUNIN', 'YAULI', 'PACCHA', 1),
  (
    '110607',
    'JUNIN',
    'YAULI',
    'SANTA BARBARA DE CARHUACAYAN',
    1
  ),
  ('110608', 'JUNIN', 'YAULI', 'SUITUCANCHA', 1),
  ('110609', 'JUNIN', 'YAULI', 'YAULI', 1),
  (
    '110610',
    'JUNIN',
    'YAULI',
    'SANTA ROSA DE SACCO',
    1
  ),
  ('110701', 'JUNIN', 'SATIPO', 'SATIPO', 1),
  ('110702', 'JUNIN', 'SATIPO', 'COVIRIALI', 1),
  ('110703', 'JUNIN', 'SATIPO', 'LLAYLLA', 1),
  ('110704', 'JUNIN', 'SATIPO', 'MAZAMARI', 1),
  ('110705', 'JUNIN', 'SATIPO', 'PAMPA HERMOSA', 1),
  ('110706', 'JUNIN', 'SATIPO', 'PANGOA', 1),
  ('110707', 'JUNIN', 'SATIPO', 'RIO NEGRO', 1),
  ('110708', 'JUNIN', 'SATIPO', 'RIO TAMBO', 1),
  (
    '110709',
    'JUNIN',
    'SATIPO',
    'VIZCATAN DEL ENE',
    1
  ),
  (
    '110801',
    'JUNIN',
    'CHANCHAMAYO',
    'CHANCHAMAYO',
    1
  ),
  ('110802', 'JUNIN', 'CHANCHAMAYO', 'SAN RAMON', 1),
  ('110803', 'JUNIN', 'CHANCHAMAYO', 'VITOC', 1),
  (
    '110804',
    'JUNIN',
    'CHANCHAMAYO',
    'SAN LUIS DE SHUARO',
    1
  ),
  (
    '110805',
    'JUNIN',
    'CHANCHAMAYO',
    'PICHANAQUI',
    1
  ),
  ('110806', 'JUNIN', 'CHANCHAMAYO', 'PERENE', 1),
  ('110901', 'JUNIN', 'CHUPACA', 'CHUPACA', 1),
  ('110902', 'JUNIN', 'CHUPACA', 'AHUAC', 1),
  ('110903', 'JUNIN', 'CHUPACA', 'CHONGOS BAJO', 1),
  ('110904', 'JUNIN', 'CHUPACA', 'HUACHAC', 1),
  (
    '110905',
    'JUNIN',
    'CHUPACA',
    'HUAMANCACA CHICO',
    1
  ),
  (
    '110906',
    'JUNIN',
    'CHUPACA',
    'SAN JUAN DE YSCOS',
    1
  ),
  (
    '110907',
    'JUNIN',
    'CHUPACA',
    'SAN JUAN DE JARPA',
    1
  ),
  (
    '110908',
    'JUNIN',
    'CHUPACA',
    'TRES DE DICIEMBRE',
    1
  ),
  ('110909', 'JUNIN', 'CHUPACA', 'YANACANCHA', 1),
  (
    '120101',
    'LA LIBERTAD',
    'TRUJILLO',
    'TRUJILLO',
    1
  ),
  (
    '120102',
    'LA LIBERTAD',
    'TRUJILLO',
    'HUANCHACO',
    1
  ),
  ('120103', 'LA LIBERTAD', 'TRUJILLO', 'LAREDO', 1),
  ('120104', 'LA LIBERTAD', 'TRUJILLO', 'MOCHE', 1),
  (
    '120105',
    'LA LIBERTAD',
    'TRUJILLO',
    'SALAVERRY',
    1
  ),
  ('120106', 'LA LIBERTAD', 'TRUJILLO', 'SIMBAL', 1),
  (
    '120107',
    'LA LIBERTAD',
    'TRUJILLO',
    'VICTOR LARCO HERRERA',
    1
  ),
  ('120109', 'LA LIBERTAD', 'TRUJILLO', 'POROTO', 1),
  (
    '120110',
    'LA LIBERTAD',
    'TRUJILLO',
    'EL PORVENIR',
    1
  ),
  (
    '120111',
    'LA LIBERTAD',
    'TRUJILLO',
    'LA ESPERANZA',
    1
  ),
  (
    '120112',
    'LA LIBERTAD',
    'TRUJILLO',
    'FLORENCIA DE MORA',
    1
  ),
  ('120201', 'LA LIBERTAD', 'BOLIVAR', 'BOLIVAR', 1),
  (
    '120202',
    'LA LIBERTAD',
    'BOLIVAR',
    'BAMBAMARCA',
    1
  ),
  (
    '120203',
    'LA LIBERTAD',
    'BOLIVAR',
    'CONDORMARCA',
    1
  ),
  (
    '120204',
    'LA LIBERTAD',
    'BOLIVAR',
    'LONGOTEA',
    1
  ),
  ('120205', 'LA LIBERTAD', 'BOLIVAR', 'UCUNCHA', 1),
  (
    '120206',
    'LA LIBERTAD',
    'BOLIVAR',
    'UCHUMARCA',
    1
  ),
  (
    '120301',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'HUAMACHUCO',
    1
  ),
  (
    '120302',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'COCHORCO',
    1
  ),
  (
    '120303',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'CURGOS',
    1
  ),
  (
    '120304',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'CHUGAY',
    1
  ),
  (
    '120305',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'MARCABAL',
    1
  ),
  (
    '120306',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'SANAGORAN',
    1
  ),
  (
    '120307',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'SARIN',
    1
  ),
  (
    '120308',
    'LA LIBERTAD',
    'SANCHEZ CARRION',
    'SARTIMBAMBA',
    1
  ),
  ('120401', 'LA LIBERTAD', 'OTUZCO', 'OTUZCO', 1),
  (
    '120402',
    'LA LIBERTAD',
    'OTUZCO',
    'AGALLPAMPA',
    1
  ),
  ('120403', 'LA LIBERTAD', 'OTUZCO', 'CHARAT', 1),
  (
    '120404',
    'LA LIBERTAD',
    'OTUZCO',
    'HUARANCHAL',
    1
  ),
  (
    '120405',
    'LA LIBERTAD',
    'OTUZCO',
    'LA CUESTA',
    1
  ),
  ('120408', 'LA LIBERTAD', 'OTUZCO', 'PARANDAY', 1),
  ('120409', 'LA LIBERTAD', 'OTUZCO', 'SALPO', 1),
  ('120410', 'LA LIBERTAD', 'OTUZCO', 'SINSICAP', 1),
  ('120411', 'LA LIBERTAD', 'OTUZCO', 'USQUIL', 1),
  ('120413', 'LA LIBERTAD', 'OTUZCO', 'MACHE', 1),
  (
    '120501',
    'LA LIBERTAD',
    'PACASMAYO',
    'SAN PEDRO DE LLOC',
    1
  ),
  (
    '120503',
    'LA LIBERTAD',
    'PACASMAYO',
    'GUADALUPE',
    1
  ),
  (
    '120504',
    'LA LIBERTAD',
    'PACASMAYO',
    'JEQUETEPEQUE',
    1
  ),
  (
    '120506',
    'LA LIBERTAD',
    'PACASMAYO',
    'PACASMAYO',
    1
  ),
  (
    '120508',
    'LA LIBERTAD',
    'PACASMAYO',
    'SAN JOSE',
    1
  ),
  ('120601', 'LA LIBERTAD', 'PATAZ', 'TAYABAMBA', 1),
  ('120602', 'LA LIBERTAD', 'PATAZ', 'BULDIBUYO', 1),
  ('120603', 'LA LIBERTAD', 'PATAZ', 'CHILLIA', 1),
  (
    '120604',
    'LA LIBERTAD',
    'PATAZ',
    'HUAYLILLAS',
    1
  ),
  (
    '120605',
    'LA LIBERTAD',
    'PATAZ',
    'HUANCASPATA',
    1
  ),
  ('120606', 'LA LIBERTAD', 'PATAZ', 'HUAYO', 1),
  ('120607', 'LA LIBERTAD', 'PATAZ', 'ONGON', 1),
  ('120608', 'LA LIBERTAD', 'PATAZ', 'PARCOY', 1),
  ('120609', 'LA LIBERTAD', 'PATAZ', 'PATAZ', 1),
  ('120610', 'LA LIBERTAD', 'PATAZ', 'PIAS', 1),
  ('120611', 'LA LIBERTAD', 'PATAZ', 'TAURIJA', 1),
  ('120612', 'LA LIBERTAD', 'PATAZ', 'URPAY', 1),
  (
    '120613',
    'LA LIBERTAD',
    'PATAZ',
    'SANTIAGO DE CHALLAS',
    1
  ),
  (
    '120701',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'SANTIAGO DE CHUCO',
    1
  ),
  (
    '120702',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'CACHICADAN',
    1
  ),
  (
    '120703',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'MOLLEBAMBA',
    1
  ),
  (
    '120704',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'MOLLEPATA',
    1
  ),
  (
    '120705',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'QUIRUVILCA',
    1
  ),
  (
    '120706',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'SANTA CRUZ DE CHUCA',
    1
  ),
  (
    '120707',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'SITABAMBA',
    1
  ),
  (
    '120708',
    'LA LIBERTAD',
    'SANTIAGO DE CHUCO',
    'ANGASMARCA',
    1
  ),
  ('120801', 'LA LIBERTAD', 'ASCOPE', 'ASCOPE', 1),
  ('120802', 'LA LIBERTAD', 'ASCOPE', 'CHICAMA', 1),
  ('120803', 'LA LIBERTAD', 'ASCOPE', 'CHOCOPE', 1),
  (
    '120804',
    'LA LIBERTAD',
    'ASCOPE',
    'SANTIAGO DE CAO',
    1
  ),
  (
    '120805',
    'LA LIBERTAD',
    'ASCOPE',
    'MAGDALENA DE CAO',
    1
  ),
  ('120806', 'LA LIBERTAD', 'ASCOPE', 'PAIJAN', 1),
  ('120807', 'LA LIBERTAD', 'ASCOPE', 'RAZURI', 1),
  (
    '120808',
    'LA LIBERTAD',
    'ASCOPE',
    'CASA GRANDE',
    1
  ),
  ('120901', 'LA LIBERTAD', 'CHEPEN', 'CHEPEN', 1),
  ('120902', 'LA LIBERTAD', 'CHEPEN', 'PACANGA', 1),
  (
    '120903',
    'LA LIBERTAD',
    'CHEPEN',
    'PUEBLO NUEVO',
    1
  ),
  ('121001', 'LA LIBERTAD', 'JULCAN', 'JULCAN', 1),
  (
    '121002',
    'LA LIBERTAD',
    'JULCAN',
    'CARABAMBA',
    1
  ),
  (
    '121003',
    'LA LIBERTAD',
    'JULCAN',
    'CALAMARCA',
    1
  ),
  ('121004', 'LA LIBERTAD', 'JULCAN', 'HUASO', 1),
  (
    '121101',
    'LA LIBERTAD',
    'GRAN CHIMU',
    'CASCAS',
    1
  ),
  (
    '121102',
    'LA LIBERTAD',
    'GRAN CHIMU',
    'LUCMA',
    1
  ),
  (
    '121103',
    'LA LIBERTAD',
    'GRAN CHIMU',
    'MARMOT',
    1
  ),
  (
    '121104',
    'LA LIBERTAD',
    'GRAN CHIMU',
    'SAYAPULLO',
    1
  ),
  ('121201', 'LA LIBERTAD', 'VIRU', 'VIRU', 1),
  ('121202', 'LA LIBERTAD', 'VIRU', 'CHAO', 1),
  (
    '121203',
    'LA LIBERTAD',
    'VIRU',
    'GUADALUPITO',
    1
  ),
  (
    '130101',
    'LAMBAYEQUE',
    'CHICLAYO',
    'CHICLAYO',
    1
  ),
  (
    '130102',
    'LAMBAYEQUE',
    'CHICLAYO',
    'CHONGOYAPE',
    1
  ),
  ('130103', 'LAMBAYEQUE', 'CHICLAYO', 'ETEN', 1),
  (
    '130104',
    'LAMBAYEQUE',
    'CHICLAYO',
    'ETEN PUERTO',
    1
  ),
  ('130105', 'LAMBAYEQUE', 'CHICLAYO', 'LAGUNAS', 1),
  ('130106', 'LAMBAYEQUE', 'CHICLAYO', 'MONSEFU', 1),
  (
    '130107',
    'LAMBAYEQUE',
    'CHICLAYO',
    'NUEVA ARICA',
    1
  ),
  ('130108', 'LAMBAYEQUE', 'CHICLAYO', 'OYOTUN', 1),
  ('130109', 'LAMBAYEQUE', 'CHICLAYO', 'PICSI', 1),
  (
    '130110',
    'LAMBAYEQUE',
    'CHICLAYO',
    'PIMENTEL',
    1
  ),
  ('130111', 'LAMBAYEQUE', 'CHICLAYO', 'REQUE', 1),
  (
    '130112',
    'LAMBAYEQUE',
    'CHICLAYO',
    'JOSE LEONARDO ORTIZ',
    1
  ),
  (
    '130113',
    'LAMBAYEQUE',
    'CHICLAYO',
    'SANTA ROSA',
    1
  ),
  ('130114', 'LAMBAYEQUE', 'CHICLAYO', 'SAÑA', 1),
  (
    '130115',
    'LAMBAYEQUE',
    'CHICLAYO',
    'LA VICTORIA',
    1
  ),
  ('130116', 'LAMBAYEQUE', 'CHICLAYO', 'CAYALTI', 1),
  ('130117', 'LAMBAYEQUE', 'CHICLAYO', 'PATAPO', 1),
  ('130118', 'LAMBAYEQUE', 'CHICLAYO', 'POMALCA', 1),
  ('130119', 'LAMBAYEQUE', 'CHICLAYO', 'PUCALA', 1),
  ('130120', 'LAMBAYEQUE', 'CHICLAYO', 'TUMAN', 1),
  (
    '130201',
    'LAMBAYEQUE',
    'FERREÑAFE',
    'FERREÑAFE',
    1
  ),
  (
    '130202',
    'LAMBAYEQUE',
    'FERREÑAFE',
    'INCAHUASI',
    1
  ),
  (
    '130203',
    'LAMBAYEQUE',
    'FERREÑAFE',
    'CAÑARIS',
    1
  ),
  ('130204', 'LAMBAYEQUE', 'FERREÑAFE', 'PITIPO', 1),
  (
    '130205',
    'LAMBAYEQUE',
    'FERREÑAFE',
    'PUEBLO NUEVO',
    1
  ),
  (
    '130206',
    'LAMBAYEQUE',
    'FERREÑAFE',
    'MANUEL ANTONIO MESONES MURO',
    1
  ),
  (
    '130301',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    1
  ),
  (
    '130302',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'CHOCHOPE',
    1
  ),
  (
    '130303',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'ILLIMO',
    1
  ),
  (
    '130304',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'JAYANCA',
    1
  ),
  (
    '130305',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'MOCHUMI',
    1
  ),
  (
    '130306',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'MORROPE',
    1
  ),
  (
    '130307',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'MOTUPE',
    1
  ),
  ('130308', 'LAMBAYEQUE', 'LAMBAYEQUE', 'OLMOS', 1),
  (
    '130309',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'PACORA',
    1
  ),
  ('130310', 'LAMBAYEQUE', 'LAMBAYEQUE', 'SALAS', 1),
  (
    '130311',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'SAN JOSE',
    1
  ),
  (
    '130312',
    'LAMBAYEQUE',
    'LAMBAYEQUE',
    'TUCUME',
    1
  ),
  ('140101', 'LIMA', 'LIMA', 'LIMA', 1),
  ('140102', 'LIMA', 'LIMA', 'ANCON', 1),
  ('140103', 'LIMA', 'LIMA', 'ATE', 1),
  ('140104', 'LIMA', 'LIMA', 'BREÑA', 1),
  ('140105', 'LIMA', 'LIMA', 'CARABAYLLO', 1),
  ('140106', 'LIMA', 'LIMA', 'COMAS', 1),
  ('140107', 'LIMA', 'LIMA', 'CHACLACAYO', 1),
  ('140108', 'LIMA', 'LIMA', 'CHORRILLOS', 1),
  ('140109', 'LIMA', 'LIMA', 'LA VICTORIA', 1),
  ('140110', 'LIMA', 'LIMA', 'LA MOLINA', 1),
  ('140111', 'LIMA', 'LIMA', 'LINCE', 1),
  ('140112', 'LIMA', 'LIMA', 'LURIGANCHO', 1),
  ('140113', 'LIMA', 'LIMA', 'LURIN', 1),
  ('140114', 'LIMA', 'LIMA', 'MAGDALENA DEL MAR', 1),
  ('140115', 'LIMA', 'LIMA', 'MIRAFLORES', 1),
  ('140116', 'LIMA', 'LIMA', 'PACHACAMAC', 1),
  ('140117', 'LIMA', 'LIMA', 'PUEBLO LIBRE', 1),
  ('140118', 'LIMA', 'LIMA', 'PUCUSANA', 1),
  ('140119', 'LIMA', 'LIMA', 'PUENTE PIEDRA', 1),
  ('140120', 'LIMA', 'LIMA', 'PUNTA HERMOSA', 1),
  ('140121', 'LIMA', 'LIMA', 'PUNTA NEGRA', 1),
  ('140122', 'LIMA', 'LIMA', 'RIMAC', 1),
  ('140123', 'LIMA', 'LIMA', 'SAN BARTOLO', 1),
  ('140124', 'LIMA', 'LIMA', 'SAN ISIDRO', 1),
  ('140125', 'LIMA', 'LIMA', 'BARRANCO', 1),
  (
    '140126',
    'LIMA',
    'LIMA',
    'SAN MARTIN DE PORRES',
    1
  ),
  ('140127', 'LIMA', 'LIMA', 'SAN MIGUEL', 1),
  (
    '140128',
    'LIMA',
    'LIMA',
    'SANTA MARIA DEL MAR',
    1
  ),
  ('140129', 'LIMA', 'LIMA', 'SANTA ROSA', 1),
  ('140130', 'LIMA', 'LIMA', 'SANTIAGO DE SURCO', 1),
  ('140131', 'LIMA', 'LIMA', 'SURQUILLO', 1),
  (
    '140132',
    'LIMA',
    'LIMA',
    'VILLA MARIA DEL TRIUNFO',
    1
  ),
  ('140133', 'LIMA', 'LIMA', 'JESUS MARIA', 1),
  ('140134', 'LIMA', 'LIMA', 'INDEPENDENCIA', 1),
  ('140135', 'LIMA', 'LIMA', 'EL AGUSTINO', 1),
  (
    '140136',
    'LIMA',
    'LIMA',
    'SAN JUAN DE MIRAFLORES',
    1
  ),
  (
    '140137',
    'LIMA',
    'LIMA',
    'SAN JUAN DE LURIGANCHO',
    1
  ),
  ('140138', 'LIMA', 'LIMA', 'SAN LUIS', 1),
  ('140139', 'LIMA', 'LIMA', 'CIENEGUILLA', 1),
  ('140140', 'LIMA', 'LIMA', 'SAN BORJA', 1),
  ('140141', 'LIMA', 'LIMA', 'VILLA EL SALVADOR', 1),
  ('140142', 'LIMA', 'LIMA', 'LOS OLIVOS', 1),
  ('140143', 'LIMA', 'LIMA', 'SANTA ANITA', 1),
  ('140201', 'LIMA', 'CAJATAMBO', 'CAJATAMBO', 1),
  ('140205', 'LIMA', 'CAJATAMBO', 'COPA', 1),
  ('140206', 'LIMA', 'CAJATAMBO', 'GORGOR', 1),
  ('140207', 'LIMA', 'CAJATAMBO', 'HUANCAPON', 1),
  ('140208', 'LIMA', 'CAJATAMBO', 'MANAS', 1),
  ('140301', 'LIMA', 'CANTA', 'CANTA', 1),
  ('140302', 'LIMA', 'CANTA', 'ARAHUAY', 1),
  ('140303', 'LIMA', 'CANTA', 'HUAMANTANGA', 1),
  ('140304', 'LIMA', 'CANTA', 'HUAROS', 1),
  ('140305', 'LIMA', 'CANTA', 'LACHAQUI', 1),
  ('140306', 'LIMA', 'CANTA', 'SAN BUENAVENTURA', 1),
  (
    '140307',
    'LIMA',
    'CANTA',
    'SANTA ROSA DE QUIVES',
    1
  ),
  (
    '140401',
    'LIMA',
    'CAÑETE',
    'SAN VICENTE DE CAÑETE',
    1
  ),
  ('140402', 'LIMA', 'CAÑETE', 'CALANGO', 1),
  ('140403', 'LIMA', 'CAÑETE', 'CERRO AZUL', 1),
  ('140404', 'LIMA', 'CAÑETE', 'COAYLLO', 1),
  ('140405', 'LIMA', 'CAÑETE', 'CHILCA', 1),
  ('140406', 'LIMA', 'CAÑETE', 'IMPERIAL', 1),
  ('140407', 'LIMA', 'CAÑETE', 'LUNAHUANA', 1),
  ('140408', 'LIMA', 'CAÑETE', 'MALA', 1),
  ('140409', 'LIMA', 'CAÑETE', 'NUEVO IMPERIAL', 1),
  ('140410', 'LIMA', 'CAÑETE', 'PACARAN', 1),
  ('140411', 'LIMA', 'CAÑETE', 'QUILMANA', 1),
  ('140412', 'LIMA', 'CAÑETE', 'SAN ANTONIO', 1),
  ('140413', 'LIMA', 'CAÑETE', 'SAN LUIS', 1),
  (
    '140414',
    'LIMA',
    'CAÑETE',
    'SANTA CRUZ DE FLORES',
    1
  ),
  ('140415', 'LIMA', 'CAÑETE', 'ZUÑIGA', 1),
  ('140416', 'LIMA', 'CAÑETE', 'ASIA', 1),
  ('140501', 'LIMA', 'HUAURA', 'HUACHO', 1),
  ('140502', 'LIMA', 'HUAURA', 'AMBAR', 1),
  (
    '140504',
    'LIMA',
    'HUAURA',
    'CALETA DE CARQUIN',
    1
  ),
  ('140505', 'LIMA', 'HUAURA', 'CHECRAS', 1),
  ('140506', 'LIMA', 'HUAURA', 'HUALMAY', 1),
  ('140507', 'LIMA', 'HUAURA', 'HUAURA', 1),
  ('140508', 'LIMA', 'HUAURA', 'LEONCIO PRADO', 1),
  ('140509', 'LIMA', 'HUAURA', 'PACCHO', 1),
  ('140511', 'LIMA', 'HUAURA', 'SANTA LEONOR', 1),
  ('140512', 'LIMA', 'HUAURA', 'SANTA MARIA', 1),
  ('140513', 'LIMA', 'HUAURA', 'SAYAN', 1),
  ('140516', 'LIMA', 'HUAURA', 'VEGUETA', 1),
  ('140601', 'LIMA', 'HUAROCHIRI', 'MATUCANA', 1),
  ('140602', 'LIMA', 'HUAROCHIRI', 'ANTIOQUIA', 1),
  ('140603', 'LIMA', 'HUAROCHIRI', 'CALLAHUANCA', 1),
  ('140604', 'LIMA', 'HUAROCHIRI', 'CARAMPOMA', 1),
  (
    '140605',
    'LIMA',
    'HUAROCHIRI',
    'SAN PEDRO DE CASTA',
    1
  ),
  ('140606', 'LIMA', 'HUAROCHIRI', 'CUENCA', 1),
  ('140607', 'LIMA', 'HUAROCHIRI', 'CHICLA', 1),
  ('140608', 'LIMA', 'HUAROCHIRI', 'HUANZA', 1),
  ('140609', 'LIMA', 'HUAROCHIRI', 'HUAROCHIRI', 1),
  ('140610', 'LIMA', 'HUAROCHIRI', 'LAHUAYTAMBO', 1),
  ('140611', 'LIMA', 'HUAROCHIRI', 'LANGA', 1),
  ('140612', 'LIMA', 'HUAROCHIRI', 'MARIATANA', 1),
  (
    '140613',
    'LIMA',
    'HUAROCHIRI',
    'RICARDO PALMA',
    1
  ),
  (
    '140614',
    'LIMA',
    'HUAROCHIRI',
    'SAN ANDRES DE TUPICOCHA',
    1
  ),
  ('140615', 'LIMA', 'HUAROCHIRI', 'SAN ANTONIO', 1),
  (
    '140616',
    'LIMA',
    'HUAROCHIRI',
    'SAN BARTOLOME',
    1
  ),
  ('140617', 'LIMA', 'HUAROCHIRI', 'SAN DAMIAN', 1),
  ('140618', 'LIMA', 'HUAROCHIRI', 'SANGALLAYA', 1),
  (
    '140619',
    'LIMA',
    'HUAROCHIRI',
    'SAN JUAN DE TANTARANCHE',
    1
  ),
  (
    '140620',
    'LIMA',
    'HUAROCHIRI',
    'SAN LORENZO DE QUINTI',
    1
  ),
  ('140621', 'LIMA', 'HUAROCHIRI', 'SAN MATEO', 1),
  (
    '140622',
    'LIMA',
    'HUAROCHIRI',
    'SAN MATEO DE OTAO',
    1
  ),
  (
    '140623',
    'LIMA',
    'HUAROCHIRI',
    'SAN PEDRO DE HUANCAYRE',
    1
  ),
  (
    '140624',
    'LIMA',
    'HUAROCHIRI',
    'SANTA CRUZ DE COCACHACRA',
    1
  ),
  (
    '140625',
    'LIMA',
    'HUAROCHIRI',
    'SANTA EULALIA',
    1
  ),
  (
    '140626',
    'LIMA',
    'HUAROCHIRI',
    'SANTIAGO DE ANCHUCAYA',
    1
  ),
  (
    '140627',
    'LIMA',
    'HUAROCHIRI',
    'SANTIAGO DE TUNA',
    1
  ),
  (
    '140628',
    'LIMA',
    'HUAROCHIRI',
    'SANTO DOMINGO DE LOS OLLEROS',
    1
  ),
  ('140629', 'LIMA', 'HUAROCHIRI', 'SURCO', 1),
  ('140630', 'LIMA', 'HUAROCHIRI', 'HUACHUPAMPA', 1),
  ('140631', 'LIMA', 'HUAROCHIRI', 'LARAOS', 1),
  (
    '140632',
    'LIMA',
    'HUAROCHIRI',
    'SAN JUAN DE IRIS',
    1
  ),
  ('140701', 'LIMA', 'YAUYOS', 'YAUYOS', 1),
  ('140702', 'LIMA', 'YAUYOS', 'ALIS', 1),
  ('140703', 'LIMA', 'YAUYOS', 'AYAUCA', 1),
  ('140704', 'LIMA', 'YAUYOS', 'AYAVIRI', 1),
  ('140705', 'LIMA', 'YAUYOS', 'AZANGARO', 1),
  ('140706', 'LIMA', 'YAUYOS', 'CACRA', 1),
  ('140707', 'LIMA', 'YAUYOS', 'CARANIA', 1),
  ('140708', 'LIMA', 'YAUYOS', 'COCHAS', 1),
  ('140709', 'LIMA', 'YAUYOS', 'COLONIA', 1),
  ('140710', 'LIMA', 'YAUYOS', 'CHOCOS', 1),
  ('140711', 'LIMA', 'YAUYOS', 'HUAMPARA', 1),
  ('140712', 'LIMA', 'YAUYOS', 'HUANCAYA', 1),
  ('140713', 'LIMA', 'YAUYOS', 'HUANGASCAR', 1),
  ('140714', 'LIMA', 'YAUYOS', 'HUANTAN', 1),
  ('140715', 'LIMA', 'YAUYOS', 'HUAÑEC', 1),
  ('140716', 'LIMA', 'YAUYOS', 'LARAOS', 1),
  ('140717', 'LIMA', 'YAUYOS', 'LINCHA', 1),
  ('140718', 'LIMA', 'YAUYOS', 'MIRAFLORES', 1),
  ('140719', 'LIMA', 'YAUYOS', 'OMAS', 1),
  ('140720', 'LIMA', 'YAUYOS', 'QUINCHES', 1),
  ('140721', 'LIMA', 'YAUYOS', 'QUINOCAY', 1),
  ('140722', 'LIMA', 'YAUYOS', 'SAN JOAQUIN', 1),
  (
    '140723',
    'LIMA',
    'YAUYOS',
    'SAN PEDRO DE PILAS',
    1
  ),
  ('140724', 'LIMA', 'YAUYOS', 'TANTA', 1),
  ('140725', 'LIMA', 'YAUYOS', 'TAURIPAMPA', 1),
  ('140726', 'LIMA', 'YAUYOS', 'TUPE', 1),
  ('140727', 'LIMA', 'YAUYOS', 'TOMAS', 1),
  ('140728', 'LIMA', 'YAUYOS', 'VIÑAC', 1),
  ('140729', 'LIMA', 'YAUYOS', 'VITIS', 1),
  ('140730', 'LIMA', 'YAUYOS', 'HONGOS', 1),
  ('140731', 'LIMA', 'YAUYOS', 'MADEAN', 1),
  ('140732', 'LIMA', 'YAUYOS', 'PUTINZA', 1),
  ('140733', 'LIMA', 'YAUYOS', 'CATAHUASI', 1),
  ('140801', 'LIMA', 'HUARAL', 'HUARAL', 1),
  ('140802', 'LIMA', 'HUARAL', 'ATAVILLOS ALTO', 1),
  ('140803', 'LIMA', 'HUARAL', 'ATAVILLOS BAJO', 1),
  ('140804', 'LIMA', 'HUARAL', 'AUCALLAMA', 1),
  ('140805', 'LIMA', 'HUARAL', 'CHANCAY', 1),
  ('140806', 'LIMA', 'HUARAL', 'IHUARI', 1),
  ('140807', 'LIMA', 'HUARAL', 'LAMPIAN', 1),
  ('140808', 'LIMA', 'HUARAL', 'PACARAOS', 1),
  (
    '140809',
    'LIMA',
    'HUARAL',
    'SAN MIGUEL DE ACOS',
    1
  ),
  (
    '140810',
    'LIMA',
    'HUARAL',
    'VEINTISIETE DE NOVIEMBRE',
    1
  ),
  (
    '140811',
    'LIMA',
    'HUARAL',
    'SANTA CRUZ DE ANDAMARCA',
    1
  ),
  ('140812', 'LIMA', 'HUARAL', 'SUMBILCA', 1),
  ('140901', 'LIMA', 'BARRANCA', 'BARRANCA', 1),
  ('140902', 'LIMA', 'BARRANCA', 'PARAMONGA', 1),
  ('140903', 'LIMA', 'BARRANCA', 'PATIVILCA', 1),
  ('140904', 'LIMA', 'BARRANCA', 'SUPE', 1),
  ('140905', 'LIMA', 'BARRANCA', 'SUPE PUERTO', 1),
  ('141001', 'LIMA', 'OYON', 'OYON', 1),
  ('141002', 'LIMA', 'OYON', 'NAVAN', 1),
  ('141003', 'LIMA', 'OYON', 'CAUJUL', 1),
  ('141004', 'LIMA', 'OYON', 'ANDAJES', 1),
  ('141005', 'LIMA', 'OYON', 'PACHANGARA', 1),
  ('141006', 'LIMA', 'OYON', 'COCHAMARCA', 1),
  ('150101', 'LORETO', 'MAYNAS', 'IQUITOS', 1),
  ('150102', 'LORETO', 'MAYNAS', 'ALTO NANAY', 1),
  (
    '150103',
    'LORETO',
    'MAYNAS',
    'FERNANDO LORES',
    1
  ),
  ('150104', 'LORETO', 'MAYNAS', 'LAS AMAZONAS', 1),
  ('150105', 'LORETO', 'MAYNAS', 'MAZAN', 1),
  ('150106', 'LORETO', 'MAYNAS', 'NAPO', 1),
  ('150107', 'LORETO', 'MAYNAS', 'PUTUMAYO', 1),
  (
    '150108',
    'LORETO',
    'MAYNAS',
    'TORRES CAUSANA',
    1
  ),
  ('150110', 'LORETO', 'MAYNAS', 'INDIANA', 1),
  ('150111', 'LORETO', 'MAYNAS', 'PUNCHANA', 1),
  ('150112', 'LORETO', 'MAYNAS', 'BELEN', 1),
  (
    '150113',
    'LORETO',
    'MAYNAS',
    'SAN JUAN BAUTISTA',
    1
  ),
  (
    '150114',
    'LORETO',
    'MAYNAS',
    'TENIENTE MANUEL CLAVERO',
    1
  ),
  (
    '150201',
    'LORETO',
    'ALTO AMAZONAS',
    'YURIMAGUAS',
    1
  ),
  (
    '150202',
    'LORETO',
    'ALTO AMAZONAS',
    'BALSAPUERTO',
    1
  ),
  (
    '150205',
    'LORETO',
    'ALTO AMAZONAS',
    'JEBEROS',
    1
  ),
  (
    '150206',
    'LORETO',
    'ALTO AMAZONAS',
    'LAGUNAS',
    1
  ),
  (
    '150210',
    'LORETO',
    'ALTO AMAZONAS',
    'SANTA CRUZ',
    1
  ),
  (
    '150211',
    'LORETO',
    'ALTO AMAZONAS',
    'TENIENTE CESAR LOPEZ ROJAS',
    1
  ),
  ('150301', 'LORETO', 'LORETO', 'NAUTA', 1),
  ('150302', 'LORETO', 'LORETO', 'PARINARI', 1),
  ('150303', 'LORETO', 'LORETO', 'TIGRE', 1),
  ('150304', 'LORETO', 'LORETO', 'URARINAS', 1),
  ('150305', 'LORETO', 'LORETO', 'TROMPETEROS', 1),
  ('150401', 'LORETO', 'REQUENA', 'REQUENA', 1),
  ('150402', 'LORETO', 'REQUENA', 'ALTO TAPICHE', 1),
  ('150403', 'LORETO', 'REQUENA', 'CAPELO', 1),
  (
    '150404',
    'LORETO',
    'REQUENA',
    'EMILIO SAN MARTIN',
    1
  ),
  ('150405', 'LORETO', 'REQUENA', 'MAQUIA', 1),
  ('150406', 'LORETO', 'REQUENA', 'PUINAHUA', 1),
  ('150407', 'LORETO', 'REQUENA', 'SAQUENA', 1),
  ('150408', 'LORETO', 'REQUENA', 'SOPLIN', 1),
  ('150409', 'LORETO', 'REQUENA', 'TAPICHE', 1),
  (
    '150410',
    'LORETO',
    'REQUENA',
    'JENARO HERRERA',
    1
  ),
  ('150411', 'LORETO', 'REQUENA', 'YAQUERANA', 1),
  ('150501', 'LORETO', 'UCAYALI', 'CONTAMANA', 1),
  (
    '150502',
    'LORETO',
    'UCAYALI',
    'VARGAS GUERRA',
    1
  ),
  (
    '150503',
    'LORETO',
    'UCAYALI',
    'PADRE MARQUEZ',
    1
  ),
  (
    '150504',
    'LORETO',
    'UCAYALI',
    'PAMPA HERMOSA',
    1
  ),
  ('150505', 'LORETO', 'UCAYALI', 'SARAYACU', 1),
  ('150506', 'LORETO', 'UCAYALI', 'INAHUAYA', 1),
  (
    '150601',
    'LORETO',
    'MARISCAL RAMON CASTILLA',
    'RAMON CASTILLA',
    1
  ),
  (
    '150602',
    'LORETO',
    'MARISCAL RAMON CASTILLA',
    'PEBAS',
    1
  ),
  (
    '150603',
    'LORETO',
    'MARISCAL RAMON CASTILLA',
    'YAVARI',
    1
  ),
  (
    '150604',
    'LORETO',
    'MARISCAL RAMON CASTILLA',
    'SAN PABLO',
    1
  ),
  (
    '150701',
    'LORETO',
    'DATEM DEL MARAÑON',
    'BARRANCA',
    1
  ),
  (
    '150702',
    'LORETO',
    'DATEM DEL MARAÑON',
    'ANDOAS',
    1
  ),
  (
    '150703',
    'LORETO',
    'DATEM DEL MARAÑON',
    'CAHUAPANAS',
    1
  ),
  (
    '150704',
    'LORETO',
    'DATEM DEL MARAÑON',
    'MANSERICHE',
    1
  ),
  (
    '150705',
    'LORETO',
    'DATEM DEL MARAÑON',
    'MORONA',
    1
  ),
  (
    '150706',
    'LORETO',
    'DATEM DEL MARAÑON',
    'PASTAZA',
    1
  ),
  ('150901', 'LORETO', 'PUTUMAYO', 'PUTUMAYO', 1),
  (
    '150902',
    'LORETO',
    'PUTUMAYO',
    'ROSA PANDURO',
    1
  ),
  (
    '150903',
    'LORETO',
    'PUTUMAYO',
    'TENIENTE MANUEL CLAVERO',
    1
  ),
  ('150904', 'LORETO', 'PUTUMAYO', 'YAGUAS', 1),
  (
    '160101',
    'MADRE DE DIOS',
    'TAMBOPATA',
    'TAMBOPATA',
    1
  ),
  (
    '160102',
    'MADRE DE DIOS',
    'TAMBOPATA',
    'INAMBARI',
    1
  ),
  (
    '160103',
    'MADRE DE DIOS',
    'TAMBOPATA',
    'LAS PIEDRAS',
    1
  ),
  (
    '160104',
    'MADRE DE DIOS',
    'TAMBOPATA',
    'LABERINTO',
    1
  ),
  ('160201', 'MADRE DE DIOS', 'MANU', 'MANU', 1),
  (
    '160202',
    'MADRE DE DIOS',
    'MANU',
    'FITZCARRALD',
    1
  ),
  (
    '160203',
    'MADRE DE DIOS',
    'MANU',
    'MADRE DE DIOS',
    1
  ),
  (
    '160204',
    'MADRE DE DIOS',
    'MANU',
    'HUEPETUHE',
    1
  ),
  (
    '160301',
    'MADRE DE DIOS',
    'TAHUAMANU',
    'IÑAPARI',
    1
  ),
  (
    '160302',
    'MADRE DE DIOS',
    'TAHUAMANU',
    'IBERIA',
    1
  ),
  (
    '160303',
    'MADRE DE DIOS',
    'TAHUAMANU',
    'TAHUAMANU',
    1
  ),
  (
    '170101',
    'MOQUEGUA',
    'MARISCAL NIETO',
    'MOQUEGUA',
    1
  ),
  (
    '170102',
    'MOQUEGUA',
    'MARISCAL NIETO',
    'CARUMAS',
    1
  ),
  (
    '170103',
    'MOQUEGUA',
    'MARISCAL NIETO',
    'CUCHUMBAYA',
    1
  ),
  (
    '170104',
    'MOQUEGUA',
    'MARISCAL NIETO',
    'SAN CRISTOBAL',
    1
  ),
  (
    '170105',
    'MOQUEGUA',
    'MARISCAL NIETO',
    'TORATA',
    1
  ),
  (
    '170106',
    'MOQUEGUA',
    'MARISCAL NIETO',
    'SAMEGUA',
    1
  ),
  (
    '170107',
    'MOQUEGUA',
    'MARISCAL NIETO',
    'SAN ANTONIO',
    1
  ),
  (
    '170201',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'OMATE',
    1
  ),
  (
    '170202',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'COALAQUE',
    1
  ),
  (
    '170203',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'CHOJATA',
    1
  ),
  (
    '170204',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'ICHUÑA',
    1
  ),
  (
    '170205',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'LA CAPILLA',
    1
  ),
  (
    '170206',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'LLOQUE',
    1
  ),
  (
    '170207',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'MATALAQUE',
    1
  ),
  (
    '170208',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'PUQUINA',
    1
  ),
  (
    '170209',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'QUINISTAQUILLAS',
    1
  ),
  (
    '170210',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'UBINAS',
    1
  ),
  (
    '170211',
    'MOQUEGUA',
    'GENERAL SANCHEZ CERRO',
    'YUNGA',
    1
  ),
  ('170301', 'MOQUEGUA', 'ILO', 'ILO', 1),
  ('170302', 'MOQUEGUA', 'ILO', 'EL ALGARROBAL', 1),
  ('170303', 'MOQUEGUA', 'ILO', 'PACOCHA', 1),
  ('180101', 'PASCO', 'PASCO', 'CHAUPIMARCA', 1),
  ('180103', 'PASCO', 'PASCO', 'HUACHON', 1),
  ('180104', 'PASCO', 'PASCO', 'HUARIACA', 1),
  ('180105', 'PASCO', 'PASCO', 'HUAYLLAY', 1),
  ('180106', 'PASCO', 'PASCO', 'NINACACA', 1),
  ('180107', 'PASCO', 'PASCO', 'PALLANCHACRA', 1),
  ('180108', 'PASCO', 'PASCO', 'PAUCARTAMBO', 1),
  (
    '180109',
    'PASCO',
    'PASCO',
    'SAN FRANCISCO DE ASIS DE YARUSYACAN',
    1
  ),
  ('180110', 'PASCO', 'PASCO', 'SIMON BOLIVAR', 1),
  ('180111', 'PASCO', 'PASCO', 'TICLACAYAN', 1),
  ('180112', 'PASCO', 'PASCO', 'TINYAHUARCO', 1),
  ('180113', 'PASCO', 'PASCO', 'VICCO', 1),
  ('180114', 'PASCO', 'PASCO', 'YANACANCHA', 1),
  (
    '180201',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'YANAHUANCA',
    1
  ),
  (
    '180202',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'CHACAYAN',
    1
  ),
  (
    '180203',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'GOYLLARISQUIZGA',
    1
  ),
  (
    '180204',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'PAUCAR',
    1
  ),
  (
    '180205',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'SAN PEDRO DE PILLAO',
    1
  ),
  (
    '180206',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'SANTA ANA DE TUSI',
    1
  ),
  (
    '180207',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'TAPUC',
    1
  ),
  (
    '180208',
    'PASCO',
    'DANIEL ALCIDES CARRION',
    'VILCABAMBA',
    1
  ),
  ('180301', 'PASCO', 'OXAPAMPA', 'OXAPAMPA', 1),
  ('180302', 'PASCO', 'OXAPAMPA', 'CHONTABAMBA', 1),
  ('180303', 'PASCO', 'OXAPAMPA', 'HUANCABAMBA', 1),
  (
    '180304',
    'PASCO',
    'OXAPAMPA',
    'PUERTO BERMUDEZ',
    1
  ),
  ('180305', 'PASCO', 'OXAPAMPA', 'VILLA RICA', 1),
  ('180306', 'PASCO', 'OXAPAMPA', 'POZUZO', 1),
  ('180307', 'PASCO', 'OXAPAMPA', 'PALCAZU', 1),
  ('180308', 'PASCO', 'OXAPAMPA', 'CONSTITUCION', 1),
  ('190101', 'PIURA', 'PIURA', 'PIURA', 1),
  ('190103', 'PIURA', 'PIURA', 'CASTILLA', 1),
  ('190104', 'PIURA', 'PIURA', 'CATACAOS', 1),
  ('190105', 'PIURA', 'PIURA', 'LA ARENA', 1),
  ('190106', 'PIURA', 'PIURA', 'LA UNION', 1),
  ('190107', 'PIURA', 'PIURA', 'LAS LOMAS', 1),
  ('190109', 'PIURA', 'PIURA', 'TAMBO GRANDE', 1),
  ('190113', 'PIURA', 'PIURA', 'CURA MORI', 1),
  ('190114', 'PIURA', 'PIURA', 'EL TALLAN', 1),
  (
    '190115',
    'PIURA',
    'PIURA',
    'VEINTISEIS DE OCTUBRE',
    1
  ),
  ('190201', 'PIURA', 'AYABACA', 'AYABACA', 1),
  ('190202', 'PIURA', 'AYABACA', 'FRIAS', 1),
  ('190203', 'PIURA', 'AYABACA', 'LAGUNAS', 1),
  ('190204', 'PIURA', 'AYABACA', 'MONTERO', 1),
  ('190205', 'PIURA', 'AYABACA', 'PACAIPAMPA', 1),
  ('190206', 'PIURA', 'AYABACA', 'SAPILLICA', 1),
  ('190207', 'PIURA', 'AYABACA', 'SICCHEZ', 1),
  ('190208', 'PIURA', 'AYABACA', 'SUYO', 1),
  ('190209', 'PIURA', 'AYABACA', 'JILILI', 1),
  ('190210', 'PIURA', 'AYABACA', 'PAIMAS', 1),
  (
    '190301',
    'PIURA',
    'HUANCABAMBA',
    'HUANCABAMBA',
    1
  ),
  ('190302', 'PIURA', 'HUANCABAMBA', 'CANCHAQUE', 1),
  ('190303', 'PIURA', 'HUANCABAMBA', 'HUARMACA', 1),
  ('190304', 'PIURA', 'HUANCABAMBA', 'SONDOR', 1),
  (
    '190305',
    'PIURA',
    'HUANCABAMBA',
    'SONDORILLO',
    1
  ),
  (
    '190306',
    'PIURA',
    'HUANCABAMBA',
    'EL CARMEN DE LA FRONTERA',
    1
  ),
  (
    '190307',
    'PIURA',
    'HUANCABAMBA',
    'SAN MIGUEL DE EL FAIQUE',
    1
  ),
  ('190308', 'PIURA', 'HUANCABAMBA', 'LALAQUIZ', 1),
  ('190401', 'PIURA', 'MORROPON', 'CHULUCANAS', 1),
  ('190402', 'PIURA', 'MORROPON', 'BUENOS AIRES', 1),
  ('190403', 'PIURA', 'MORROPON', 'CHALACO', 1),
  ('190404', 'PIURA', 'MORROPON', 'MORROPON', 1),
  ('190405', 'PIURA', 'MORROPON', 'SALITRAL', 1),
  (
    '190406',
    'PIURA',
    'MORROPON',
    'SANTA CATALINA DE MOSSA',
    1
  ),
  (
    '190407',
    'PIURA',
    'MORROPON',
    'SANTO DOMINGO',
    1
  ),
  ('190408', 'PIURA', 'MORROPON', 'LA MATANZA', 1),
  ('190409', 'PIURA', 'MORROPON', 'YAMANGO', 1),
  (
    '190410',
    'PIURA',
    'MORROPON',
    'SAN JUAN DE BIGOTE',
    1
  ),
  ('190501', 'PIURA', 'PAITA', 'PAITA', 1),
  ('190502', 'PIURA', 'PAITA', 'AMOTAPE', 1),
  ('190503', 'PIURA', 'PAITA', 'ARENAL', 1),
  ('190504', 'PIURA', 'PAITA', 'LA HUACA', 1),
  ('190505', 'PIURA', 'PAITA', 'COLAN', 1),
  ('190506', 'PIURA', 'PAITA', 'TAMARINDO', 1),
  ('190507', 'PIURA', 'PAITA', 'VICHAYAL', 1),
  ('190601', 'PIURA', 'SULLANA', 'SULLANA', 1),
  ('190602', 'PIURA', 'SULLANA', 'BELLAVISTA', 1),
  ('190603', 'PIURA', 'SULLANA', 'LANCONES', 1),
  ('190604', 'PIURA', 'SULLANA', 'MARCAVELICA', 1),
  ('190605', 'PIURA', 'SULLANA', 'MIGUEL CHECA', 1),
  ('190606', 'PIURA', 'SULLANA', 'QUERECOTILLO', 1),
  ('190607', 'PIURA', 'SULLANA', 'SALITRAL', 1),
  (
    '190608',
    'PIURA',
    'SULLANA',
    'IGNACIO ESCUDERO',
    1
  ),
  ('190701', 'PIURA', 'TALARA', 'PARIÑAS', 1),
  ('190702', 'PIURA', 'TALARA', 'EL ALTO', 1),
  ('190703', 'PIURA', 'TALARA', 'LA BREA', 1),
  ('190704', 'PIURA', 'TALARA', 'LOBITOS', 1),
  ('190705', 'PIURA', 'TALARA', 'MANCORA', 1),
  ('190706', 'PIURA', 'TALARA', 'LOS ORGANOS', 1),
  ('190801', 'PIURA', 'SECHURA', 'SECHURA', 1),
  ('190802', 'PIURA', 'SECHURA', 'VICE', 1),
  ('190803', 'PIURA', 'SECHURA', 'BERNAL', 1),
  (
    '190804',
    'PIURA',
    'SECHURA',
    'BELLAVISTA DE LA UNION',
    1
  ),
  (
    '190805',
    'PIURA',
    'SECHURA',
    'CRISTO NOS VALGA',
    1
  ),
  (
    '190806',
    'PIURA',
    'SECHURA',
    'RINCONADA LLICUAR',
    1
  ),
  ('200101', 'PUNO', 'PUNO', 'PUNO', 1),
  ('200102', 'PUNO', 'PUNO', 'ACORA', 1),
  ('200103', 'PUNO', 'PUNO', 'ATUNCOLLA', 1),
  ('200104', 'PUNO', 'PUNO', 'CAPACHICA', 1),
  ('200105', 'PUNO', 'PUNO', 'COATA', 1),
  ('200106', 'PUNO', 'PUNO', 'CHUCUITO', 1),
  ('200107', 'PUNO', 'PUNO', 'HUATA', 1),
  ('200108', 'PUNO', 'PUNO', 'MAÑAZO', 1),
  ('200109', 'PUNO', 'PUNO', 'PAUCARCOLLA', 1),
  ('200110', 'PUNO', 'PUNO', 'PICHACANI', 1),
  ('200111', 'PUNO', 'PUNO', 'SAN ANTONIO', 1),
  ('200112', 'PUNO', 'PUNO', 'TIQUILLACA', 1),
  ('200113', 'PUNO', 'PUNO', 'VILQUE', 1),
  ('200114', 'PUNO', 'PUNO', 'PLATERIA', 1),
  ('200115', 'PUNO', 'PUNO', 'AMANTANI', 1),
  ('200201', 'PUNO', 'AZANGARO', 'AZANGARO', 1),
  ('200202', 'PUNO', 'AZANGARO', 'ACHAYA', 1),
  ('200203', 'PUNO', 'AZANGARO', 'ARAPA', 1),
  ('200204', 'PUNO', 'AZANGARO', 'ASILLO', 1),
  ('200205', 'PUNO', 'AZANGARO', 'CAMINACA', 1),
  ('200206', 'PUNO', 'AZANGARO', 'CHUPA', 1),
  (
    '200207',
    'PUNO',
    'AZANGARO',
    'JOSE DOMINGO CHOQUEHUANCA',
    1
  ),
  ('200208', 'PUNO', 'AZANGARO', 'MUÑANI', 1),
  ('200210', 'PUNO', 'AZANGARO', 'POTONI', 1),
  ('200212', 'PUNO', 'AZANGARO', 'SAMAN', 1),
  ('200213', 'PUNO', 'AZANGARO', 'SAN ANTON', 1),
  ('200214', 'PUNO', 'AZANGARO', 'SAN JOSE', 1),
  (
    '200215',
    'PUNO',
    'AZANGARO',
    'SAN JUAN DE SALINAS',
    1
  ),
  (
    '200216',
    'PUNO',
    'AZANGARO',
    'SANTIAGO DE PUPUJA',
    1
  ),
  ('200217', 'PUNO', 'AZANGARO', 'TIRAPATA', 1),
  ('200301', 'PUNO', 'CARABAYA', 'MACUSANI', 1),
  ('200302', 'PUNO', 'CARABAYA', 'AJOYANI', 1),
  ('200303', 'PUNO', 'CARABAYA', 'AYAPATA', 1),
  ('200304', 'PUNO', 'CARABAYA', 'COASA', 1),
  ('200305', 'PUNO', 'CARABAYA', 'CORANI', 1),
  ('200306', 'PUNO', 'CARABAYA', 'CRUCERO', 1),
  ('200307', 'PUNO', 'CARABAYA', 'ITUATA', 1),
  ('200308', 'PUNO', 'CARABAYA', 'OLLACHEA', 1),
  ('200309', 'PUNO', 'CARABAYA', 'SAN GABAN', 1),
  ('200310', 'PUNO', 'CARABAYA', 'USICAYOS', 1),
  ('200401', 'PUNO', 'CHUCUITO', 'JULI', 1),
  ('200402', 'PUNO', 'CHUCUITO', 'DESAGUADERO', 1),
  ('200403', 'PUNO', 'CHUCUITO', 'HUACULLANI', 1),
  ('200406', 'PUNO', 'CHUCUITO', 'PISACOMA', 1),
  ('200407', 'PUNO', 'CHUCUITO', 'POMATA', 1),
  ('200410', 'PUNO', 'CHUCUITO', 'ZEPITA', 1),
  ('200412', 'PUNO', 'CHUCUITO', 'KELLUYO', 1),
  ('200501', 'PUNO', 'HUANCANE', 'HUANCANE', 1),
  ('200502', 'PUNO', 'HUANCANE', 'COJATA', 1),
  ('200504', 'PUNO', 'HUANCANE', 'INCHUPALLA', 1),
  ('200506', 'PUNO', 'HUANCANE', 'PUSI', 1),
  ('200507', 'PUNO', 'HUANCANE', 'ROSASPATA', 1),
  ('200508', 'PUNO', 'HUANCANE', 'TARACO', 1),
  ('200509', 'PUNO', 'HUANCANE', 'VILQUE CHICO', 1),
  ('200511', 'PUNO', 'HUANCANE', 'HUATASANI', 1),
  ('200601', 'PUNO', 'LAMPA', 'LAMPA', 1),
  ('200602', 'PUNO', 'LAMPA', 'CABANILLA', 1),
  ('200603', 'PUNO', 'LAMPA', 'CALAPUJA', 1),
  ('200604', 'PUNO', 'LAMPA', 'NICASIO', 1),
  ('200605', 'PUNO', 'LAMPA', 'OCUVIRI', 1),
  ('200606', 'PUNO', 'LAMPA', 'PALCA', 1),
  ('200607', 'PUNO', 'LAMPA', 'PARATIA', 1),
  ('200608', 'PUNO', 'LAMPA', 'PUCARA', 1),
  ('200609', 'PUNO', 'LAMPA', 'SANTA LUCIA', 1),
  ('200610', 'PUNO', 'LAMPA', 'VILAVILA', 1),
  ('200701', 'PUNO', 'MELGAR', 'AYAVIRI', 1),
  ('200702', 'PUNO', 'MELGAR', 'ANTAUTA', 1),
  ('200703', 'PUNO', 'MELGAR', 'CUPI', 1),
  ('200704', 'PUNO', 'MELGAR', 'LLALLI', 1),
  ('200705', 'PUNO', 'MELGAR', 'MACARI', 1),
  ('200706', 'PUNO', 'MELGAR', 'NUÑOA', 1),
  ('200707', 'PUNO', 'MELGAR', 'ORURILLO', 1),
  ('200708', 'PUNO', 'MELGAR', 'SANTA ROSA', 1),
  ('200709', 'PUNO', 'MELGAR', 'UMACHIRI', 1),
  ('200801', 'PUNO', 'SANDIA', 'SANDIA', 1),
  ('200803', 'PUNO', 'SANDIA', 'CUYOCUYO', 1),
  ('200804', 'PUNO', 'SANDIA', 'LIMBANI', 1),
  ('200805', 'PUNO', 'SANDIA', 'PHARA', 1),
  ('200806', 'PUNO', 'SANDIA', 'PATAMBUCO', 1),
  ('200807', 'PUNO', 'SANDIA', 'QUIACA', 1),
  (
    '200808',
    'PUNO',
    'SANDIA',
    'SAN JUAN DEL ORO',
    1
  ),
  ('200810', 'PUNO', 'SANDIA', 'YANAHUAYA', 1),
  ('200811', 'PUNO', 'SANDIA', 'ALTO INAMBARI', 1),
  (
    '200812',
    'PUNO',
    'SANDIA',
    'SAN PEDRO DE PUTINA PUNCO',
    1
  ),
  ('200901', 'PUNO', 'SAN ROMAN', 'JULIACA', 1),
  ('200902', 'PUNO', 'SAN ROMAN', 'CABANA', 1),
  ('200903', 'PUNO', 'SAN ROMAN', 'CABANILLAS', 1),
  ('200904', 'PUNO', 'SAN ROMAN', 'CARACOTO', 1),
  ('200905', 'PUNO', 'SAN ROMAN', 'SAN MIGUEL', 1),
  ('201001', 'PUNO', 'YUNGUYO', 'YUNGUYO', 1),
  ('201002', 'PUNO', 'YUNGUYO', 'UNICACHI', 1),
  ('201003', 'PUNO', 'YUNGUYO', 'ANAPIA', 1),
  ('201004', 'PUNO', 'YUNGUYO', 'COPANI', 1),
  ('201005', 'PUNO', 'YUNGUYO', 'CUTURAPI', 1),
  ('201006', 'PUNO', 'YUNGUYO', 'OLLARAYA', 1),
  ('201007', 'PUNO', 'YUNGUYO', 'TINICACHI', 1),
  ('20101', 'ANCASH', 'HUARAZ', 'HUARAZ', 1),
  ('20102', 'ANCASH', 'HUARAZ', 'INDEPENDENCIA', 1),
  ('20103', 'ANCASH', 'HUARAZ', 'COCHABAMBA', 1),
  ('20104', 'ANCASH', 'HUARAZ', 'COLCABAMBA', 1),
  ('20105', 'ANCASH', 'HUARAZ', 'HUANCHAY', 1),
  ('20106', 'ANCASH', 'HUARAZ', 'JANGAS', 1),
  ('20107', 'ANCASH', 'HUARAZ', 'LA LIBERTAD', 1),
  ('20108', 'ANCASH', 'HUARAZ', 'OLLEROS', 1),
  ('20109', 'ANCASH', 'HUARAZ', 'PAMPAS', 1),
  ('20110', 'ANCASH', 'HUARAZ', 'PARIACOTO', 1),
  (
    '201101',
    'PUNO',
    'SAN ANTONIO DE PUTINA',
    'PUTINA',
    1
  ),
  (
    '201102',
    'PUNO',
    'SAN ANTONIO DE PUTINA',
    'PEDRO VILCA APAZA',
    1
  ),
  (
    '201103',
    'PUNO',
    'SAN ANTONIO DE PUTINA',
    'QUILCAPUNCU',
    1
  ),
  (
    '201104',
    'PUNO',
    'SAN ANTONIO DE PUTINA',
    'ANANEA',
    1
  ),
  (
    '201105',
    'PUNO',
    'SAN ANTONIO DE PUTINA',
    'SINA',
    1
  ),
  ('20111', 'ANCASH', 'HUARAZ', 'PIRA', 1),
  ('20112', 'ANCASH', 'HUARAZ', 'TARICA', 1),
  ('201201', 'PUNO', 'EL COLLAO', 'ILAVE', 1),
  ('201202', 'PUNO', 'EL COLLAO', 'PILCUYO', 1),
  ('201203', 'PUNO', 'EL COLLAO', 'SANTA ROSA', 1),
  ('201204', 'PUNO', 'EL COLLAO', 'CAPAZO', 1),
  ('201205', 'PUNO', 'EL COLLAO', 'CONDURIRI', 1),
  ('201301', 'PUNO', 'MOHO', 'MOHO', 1),
  ('201302', 'PUNO', 'MOHO', 'CONIMA', 1),
  ('201303', 'PUNO', 'MOHO', 'TILALI', 1),
  ('201304', 'PUNO', 'MOHO', 'HUAYRAPATA', 1),
  ('20201', 'ANCASH', 'AIJA', 'AIJA', 1),
  ('20203', 'ANCASH', 'AIJA', 'CORIS', 1),
  ('20205', 'ANCASH', 'AIJA', 'HUACLLAN', 1),
  ('20206', 'ANCASH', 'AIJA', 'LA MERCED', 1),
  ('20208', 'ANCASH', 'AIJA', 'SUCCHA', 1),
  ('20301', 'ANCASH', 'BOLOGNESI', 'CHIQUIAN', 1),
  (
    '20302',
    'ANCASH',
    'BOLOGNESI',
    'ABELARDO PARDO LEZAMETA',
    1
  ),
  ('20304', 'ANCASH', 'BOLOGNESI', 'AQUIA', 1),
  ('20305', 'ANCASH', 'BOLOGNESI', 'CAJACAY', 1),
  (
    '20310',
    'ANCASH',
    'BOLOGNESI',
    'HUAYLLACAYAN',
    1
  ),
  ('20311', 'ANCASH', 'BOLOGNESI', 'HUASTA', 1),
  ('20313', 'ANCASH', 'BOLOGNESI', 'MANGAS', 1),
  ('20315', 'ANCASH', 'BOLOGNESI', 'PACLLON', 1),
  (
    '20317',
    'ANCASH',
    'BOLOGNESI',
    'SAN MIGUEL DE CORPANQUI',
    1
  ),
  ('20320', 'ANCASH', 'BOLOGNESI', 'TICLLOS', 1),
  (
    '20321',
    'ANCASH',
    'BOLOGNESI',
    'ANTONIO RAYMONDI',
    1
  ),
  ('20322', 'ANCASH', 'BOLOGNESI', 'CANIS', 1),
  ('20323', 'ANCASH', 'BOLOGNESI', 'COLQUIOC', 1),
  (
    '20324',
    'ANCASH',
    'BOLOGNESI',
    'LA PRIMAVERA',
    1
  ),
  ('20325', 'ANCASH', 'BOLOGNESI', 'HUALLANCA', 1),
  ('20401', 'ANCASH', 'CARHUAZ', 'CARHUAZ', 1),
  ('20402', 'ANCASH', 'CARHUAZ', 'ACOPAMPA', 1),
  ('20403', 'ANCASH', 'CARHUAZ', 'AMASHCA', 1),
  ('20404', 'ANCASH', 'CARHUAZ', 'ANTA', 1),
  ('20405', 'ANCASH', 'CARHUAZ', 'ATAQUERO', 1),
  ('20406', 'ANCASH', 'CARHUAZ', 'MARCARA', 1),
  ('20407', 'ANCASH', 'CARHUAZ', 'PARIAHUANCA', 1),
  (
    '20408',
    'ANCASH',
    'CARHUAZ',
    'SAN MIGUEL DE ACO',
    1
  ),
  ('20409', 'ANCASH', 'CARHUAZ', 'SHILLA', 1),
  ('20410', 'ANCASH', 'CARHUAZ', 'TINCO', 1),
  ('20411', 'ANCASH', 'CARHUAZ', 'YUNGAR', 1),
  ('20501', 'ANCASH', 'CASMA', 'CASMA', 1),
  (
    '20502',
    'ANCASH',
    'CASMA',
    'BUENA VISTA ALTA',
    1
  ),
  ('20503', 'ANCASH', 'CASMA', 'COMANDANTE NOEL', 1),
  ('20505', 'ANCASH', 'CASMA', 'YAUTAN', 1),
  ('20601', 'ANCASH', 'CORONGO', 'CORONGO', 1),
  ('20602', 'ANCASH', 'CORONGO', 'ACO', 1),
  ('20603', 'ANCASH', 'CORONGO', 'BAMBAS', 1),
  ('20604', 'ANCASH', 'CORONGO', 'CUSCA', 1),
  ('20605', 'ANCASH', 'CORONGO', 'LA PAMPA', 1),
  ('20606', 'ANCASH', 'CORONGO', 'YANAC', 1),
  ('20607', 'ANCASH', 'CORONGO', 'YUPAN', 1),
  ('20701', 'ANCASH', 'HUAYLAS', 'CARAZ', 1),
  ('20702', 'ANCASH', 'HUAYLAS', 'HUALLANCA', 1),
  ('20703', 'ANCASH', 'HUAYLAS', 'HUATA', 1),
  ('20704', 'ANCASH', 'HUAYLAS', 'HUAYLAS', 1),
  ('20705', 'ANCASH', 'HUAYLAS', 'MATO', 1),
  ('20706', 'ANCASH', 'HUAYLAS', 'PAMPAROMAS', 1),
  ('20707', 'ANCASH', 'HUAYLAS', 'PUEBLO LIBRE', 1),
  ('20708', 'ANCASH', 'HUAYLAS', 'SANTA CRUZ', 1),
  ('20709', 'ANCASH', 'HUAYLAS', 'YURACMARCA', 1),
  ('20710', 'ANCASH', 'HUAYLAS', 'SANTO TORIBIO', 1),
  ('20801', 'ANCASH', 'HUARI', 'HUARI', 1),
  ('20802', 'ANCASH', 'HUARI', 'CAJAY', 1),
  (
    '20803',
    'ANCASH',
    'HUARI',
    'CHAVIN DE HUANTAR',
    1
  ),
  ('20804', 'ANCASH', 'HUARI', 'HUACACHI', 1),
  ('20805', 'ANCASH', 'HUARI', 'HUACHIS', 1),
  ('20806', 'ANCASH', 'HUARI', 'HUACCHIS', 1),
  ('20807', 'ANCASH', 'HUARI', 'HUANTAR', 1),
  ('20808', 'ANCASH', 'HUARI', 'MASIN', 1),
  ('20809', 'ANCASH', 'HUARI', 'PAUCAS', 1),
  ('20810', 'ANCASH', 'HUARI', 'PONTO', 1),
  ('20811', 'ANCASH', 'HUARI', 'RAHUAPAMPA', 1),
  ('20812', 'ANCASH', 'HUARI', 'RAPAYAN', 1),
  ('20813', 'ANCASH', 'HUARI', 'SAN MARCOS', 1),
  (
    '20814',
    'ANCASH',
    'HUARI',
    'SAN PEDRO DE CHANA',
    1
  ),
  ('20815', 'ANCASH', 'HUARI', 'UCO', 1),
  ('20816', 'ANCASH', 'HUARI', 'ANRA', 1),
  (
    '20901',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'PISCOBAMBA',
    1
  ),
  (
    '20902',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'CASCA',
    1
  ),
  (
    '20903',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'LUCMA',
    1
  ),
  (
    '20904',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'FIDEL OLIVAS ESCUDERO',
    1
  ),
  (
    '20905',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'LLAMA',
    1
  ),
  (
    '20906',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'LLUMPA',
    1
  ),
  (
    '20907',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'MUSGA',
    1
  ),
  (
    '20908',
    'ANCASH',
    'MARISCAL LUZURIAGA',
    'ELEAZAR GUZMAN BARRON',
    1
  ),
  ('21001', 'ANCASH', 'PALLASCA', 'CABANA', 1),
  ('21002', 'ANCASH', 'PALLASCA', 'BOLOGNESI', 1),
  ('21003', 'ANCASH', 'PALLASCA', 'CONCHUCOS', 1),
  ('21004', 'ANCASH', 'PALLASCA', 'HUACASCHUQUE', 1),
  ('21005', 'ANCASH', 'PALLASCA', 'HUANDOVAL', 1),
  ('21006', 'ANCASH', 'PALLASCA', 'LACABAMBA', 1),
  ('21007', 'ANCASH', 'PALLASCA', 'LLAPO', 1),
  ('21008', 'ANCASH', 'PALLASCA', 'PALLASCA', 1),
  ('21009', 'ANCASH', 'PALLASCA', 'PAMPAS', 1),
  ('21010', 'ANCASH', 'PALLASCA', 'SANTA ROSA', 1),
  (
    '210101',
    'SAN MARTIN',
    'MOYOBAMBA',
    'MOYOBAMBA',
    1
  ),
  (
    '210102',
    'SAN MARTIN',
    'MOYOBAMBA',
    'CALZADA',
    1
  ),
  ('210103', 'SAN MARTIN', 'MOYOBAMBA', 'HABANA', 1),
  (
    '210104',
    'SAN MARTIN',
    'MOYOBAMBA',
    'JEPELACIO',
    1
  ),
  (
    '210105',
    'SAN MARTIN',
    'MOYOBAMBA',
    'SORITOR',
    1
  ),
  (
    '210106',
    'SAN MARTIN',
    'MOYOBAMBA',
    'YANTALO',
    1
  ),
  ('21011', 'ANCASH', 'PALLASCA', 'TAUCA', 1),
  ('210201', 'SAN MARTIN', 'HUALLAGA', 'SAPOSOA', 1),
  (
    '210202',
    'SAN MARTIN',
    'HUALLAGA',
    'PISCOYACU',
    1
  ),
  (
    '210203',
    'SAN MARTIN',
    'HUALLAGA',
    'SACANCHE',
    1
  ),
  (
    '210204',
    'SAN MARTIN',
    'HUALLAGA',
    'TINGO DE SAPOSOA',
    1
  ),
  (
    '210205',
    'SAN MARTIN',
    'HUALLAGA',
    'ALTO SAPOSOA',
    1
  ),
  (
    '210206',
    'SAN MARTIN',
    'HUALLAGA',
    'EL ESLABON',
    1
  ),
  ('210301', 'SAN MARTIN', 'LAMAS', 'LAMAS', 1),
  (
    '210303',
    'SAN MARTIN',
    'LAMAS',
    'BARRANQUITA',
    1
  ),
  ('210304', 'SAN MARTIN', 'LAMAS', 'CAYNARACHI', 1),
  ('210305', 'SAN MARTIN', 'LAMAS', 'CUÑUMBUQUI', 1),
  (
    '210306',
    'SAN MARTIN',
    'LAMAS',
    'PINTO RECODO',
    1
  ),
  ('210307', 'SAN MARTIN', 'LAMAS', 'RUMISAPA', 1),
  ('210311', 'SAN MARTIN', 'LAMAS', 'SHANAO', 1),
  ('210313', 'SAN MARTIN', 'LAMAS', 'TABALOSOS', 1),
  ('210314', 'SAN MARTIN', 'LAMAS', 'ZAPATERO', 1),
  (
    '210315',
    'SAN MARTIN',
    'LAMAS',
    'ALONSO DE ALVARADO',
    1
  ),
  (
    '210316',
    'SAN MARTIN',
    'LAMAS',
    'SAN ROQUE DE CUMBAZA',
    1
  ),
  (
    '210401',
    'SAN MARTIN',
    'MARISCAL CACERES',
    'JUANJUI',
    1
  ),
  (
    '210402',
    'SAN MARTIN',
    'MARISCAL CACERES',
    'CAMPANILLA',
    1
  ),
  (
    '210403',
    'SAN MARTIN',
    'MARISCAL CACERES',
    'HUICUNGO',
    1
  ),
  (
    '210404',
    'SAN MARTIN',
    'MARISCAL CACERES',
    'PACHIZA',
    1
  ),
  (
    '210405',
    'SAN MARTIN',
    'MARISCAL CACERES',
    'PAJARILLO',
    1
  ),
  ('210501', 'SAN MARTIN', 'RIOJA', 'RIOJA', 1),
  ('210502', 'SAN MARTIN', 'RIOJA', 'POSIC', 1),
  ('210503', 'SAN MARTIN', 'RIOJA', 'YORONGOS', 1),
  ('210504', 'SAN MARTIN', 'RIOJA', 'YURACYACU', 1),
  (
    '210505',
    'SAN MARTIN',
    'RIOJA',
    'NUEVA CAJAMARCA',
    1
  ),
  (
    '210506',
    'SAN MARTIN',
    'RIOJA',
    'ELIAS SOPLIN VARGAS',
    1
  ),
  (
    '210507',
    'SAN MARTIN',
    'RIOJA',
    'SAN FERNANDO',
    1
  ),
  (
    '210508',
    'SAN MARTIN',
    'RIOJA',
    'PARDO MIGUEL',
    1
  ),
  ('210509', 'SAN MARTIN', 'RIOJA', 'AWAJUN', 1),
  (
    '210601',
    'SAN MARTIN',
    'SAN MARTIN',
    'TARAPOTO',
    1
  ),
  (
    '210602',
    'SAN MARTIN',
    'SAN MARTIN',
    'ALBERTO LEVEAU',
    1
  ),
  (
    '210604',
    'SAN MARTIN',
    'SAN MARTIN',
    'CACATACHI',
    1
  ),
  (
    '210606',
    'SAN MARTIN',
    'SAN MARTIN',
    'CHAZUTA',
    1
  ),
  (
    '210607',
    'SAN MARTIN',
    'SAN MARTIN',
    'CHIPURANA',
    1
  ),
  (
    '210608',
    'SAN MARTIN',
    'SAN MARTIN',
    'EL PORVENIR',
    1
  ),
  (
    '210609',
    'SAN MARTIN',
    'SAN MARTIN',
    'HUIMBAYOC',
    1
  ),
  (
    '210610',
    'SAN MARTIN',
    'SAN MARTIN',
    'JUAN GUERRA',
    1
  ),
  (
    '210611',
    'SAN MARTIN',
    'SAN MARTIN',
    'MORALES',
    1
  ),
  (
    '210612',
    'SAN MARTIN',
    'SAN MARTIN',
    'PAPAPLAYA',
    1
  ),
  (
    '210616',
    'SAN MARTIN',
    'SAN MARTIN',
    'SAN ANTONIO',
    1
  ),
  ('210619', 'SAN MARTIN', 'SAN MARTIN', 'SAUCE', 1),
  (
    '210620',
    'SAN MARTIN',
    'SAN MARTIN',
    'SHAPAJA',
    1
  ),
  (
    '210621',
    'SAN MARTIN',
    'SAN MARTIN',
    'LA BANDA DE SHILCAYO',
    1
  ),
  (
    '210701',
    'SAN MARTIN',
    'BELLAVISTA',
    'BELLAVISTA',
    1
  ),
  (
    '210702',
    'SAN MARTIN',
    'BELLAVISTA',
    'SAN RAFAEL',
    1
  ),
  (
    '210703',
    'SAN MARTIN',
    'BELLAVISTA',
    'SAN PABLO',
    1
  ),
  (
    '210704',
    'SAN MARTIN',
    'BELLAVISTA',
    'ALTO BIAVO',
    1
  ),
  (
    '210705',
    'SAN MARTIN',
    'BELLAVISTA',
    'HUALLAGA',
    1
  ),
  (
    '210706',
    'SAN MARTIN',
    'BELLAVISTA',
    'BAJO BIAVO',
    1
  ),
  ('210801', 'SAN MARTIN', 'TOCACHE', 'TOCACHE', 1),
  (
    '210802',
    'SAN MARTIN',
    'TOCACHE',
    'NUEVO PROGRESO',
    1
  ),
  ('210803', 'SAN MARTIN', 'TOCACHE', 'POLVORA', 1),
  ('210804', 'SAN MARTIN', 'TOCACHE', 'SHUNTE', 1),
  ('210805', 'SAN MARTIN', 'TOCACHE', 'UCHIZA', 1),
  (
    '210806',
    'SAN MARTIN',
    'TOCACHE',
    'SANTA LUCIA',
    1
  ),
  ('210901', 'SAN MARTIN', 'PICOTA', 'PICOTA', 1),
  (
    '210902',
    'SAN MARTIN',
    'PICOTA',
    'BUENOS AIRES',
    1
  ),
  ('210903', 'SAN MARTIN', 'PICOTA', 'CASPISAPA', 1),
  ('210904', 'SAN MARTIN', 'PICOTA', 'PILLUANA', 1),
  ('210905', 'SAN MARTIN', 'PICOTA', 'PUCACACA', 1),
  (
    '210906',
    'SAN MARTIN',
    'PICOTA',
    'SAN CRISTOBAL',
    1
  ),
  (
    '210907',
    'SAN MARTIN',
    'PICOTA',
    'SAN HILARION',
    1
  ),
  (
    '210908',
    'SAN MARTIN',
    'PICOTA',
    'TINGO DE PONASA',
    1
  ),
  (
    '210909',
    'SAN MARTIN',
    'PICOTA',
    'TRES UNIDOS',
    1
  ),
  (
    '210910',
    'SAN MARTIN',
    'PICOTA',
    'SHAMBOYACU',
    1
  ),
  (
    '211001',
    'SAN MARTIN',
    'EL DORADO',
    'SAN JOSE DE SISA',
    1
  ),
  (
    '211002',
    'SAN MARTIN',
    'EL DORADO',
    'AGUA BLANCA',
    1
  ),
  (
    '211003',
    'SAN MARTIN',
    'EL DORADO',
    'SHATOJA',
    1
  ),
  (
    '211004',
    'SAN MARTIN',
    'EL DORADO',
    'SAN MARTIN',
    1
  ),
  (
    '211005',
    'SAN MARTIN',
    'EL DORADO',
    'SANTA ROSA',
    1
  ),
  ('21101', 'ANCASH', 'POMABAMBA', 'POMABAMBA', 1),
  ('21102', 'ANCASH', 'POMABAMBA', 'HUAYLLAN', 1),
  ('21103', 'ANCASH', 'POMABAMBA', 'PAROBAMBA', 1),
  ('21104', 'ANCASH', 'POMABAMBA', 'QUINUABAMBA', 1),
  ('21201', 'ANCASH', 'RECUAY', 'RECUAY', 1),
  ('21202', 'ANCASH', 'RECUAY', 'COTAPARACO', 1),
  ('21203', 'ANCASH', 'RECUAY', 'HUAYLLAPAMPA', 1),
  ('21204', 'ANCASH', 'RECUAY', 'MARCA', 1),
  ('21205', 'ANCASH', 'RECUAY', 'PAMPAS CHICO', 1),
  ('21206', 'ANCASH', 'RECUAY', 'PARARIN', 1),
  ('21207', 'ANCASH', 'RECUAY', 'TAPACOCHA', 1),
  ('21208', 'ANCASH', 'RECUAY', 'TICAPAMPA', 1),
  ('21209', 'ANCASH', 'RECUAY', 'LLACLLIN', 1),
  ('21210', 'ANCASH', 'RECUAY', 'CATAC', 1),
  ('21301', 'ANCASH', 'SANTA', 'CHIMBOTE', 1),
  (
    '21302',
    'ANCASH',
    'SANTA',
    'CACERES DEL PERU',
    1
  ),
  ('21303', 'ANCASH', 'SANTA', 'MACATE', 1),
  ('21304', 'ANCASH', 'SANTA', 'MORO', 1),
  ('21305', 'ANCASH', 'SANTA', 'NEPEÑA', 1),
  ('21306', 'ANCASH', 'SANTA', 'SAMANCO', 1),
  ('21307', 'ANCASH', 'SANTA', 'SANTA', 1),
  ('21308', 'ANCASH', 'SANTA', 'COISHCO', 1),
  ('21309', 'ANCASH', 'SANTA', 'NUEVO CHIMBOTE', 1),
  ('21401', 'ANCASH', 'SIHUAS', 'SIHUAS', 1),
  ('21402', 'ANCASH', 'SIHUAS', 'ALFONSO UGARTE', 1),
  ('21403', 'ANCASH', 'SIHUAS', 'CHINGALPO', 1),
  ('21404', 'ANCASH', 'SIHUAS', 'HUAYLLABAMBA', 1),
  ('21405', 'ANCASH', 'SIHUAS', 'QUICHES', 1),
  ('21406', 'ANCASH', 'SIHUAS', 'SICSIBAMBA', 1);
INSERT INTO `ubigeo` (
    `codigo`,
    `departamento`,
    `provincia`,
    `distrito`,
    `activo`
  )
VALUES ('21407', 'ANCASH', 'SIHUAS', 'ACOBAMBA', 1),
  ('21408', 'ANCASH', 'SIHUAS', 'CASHAPAMPA', 1),
  ('21409', 'ANCASH', 'SIHUAS', 'RAGASH', 1),
  ('21410', 'ANCASH', 'SIHUAS', 'SAN JUAN', 1),
  ('21501', 'ANCASH', 'YUNGAY', 'YUNGAY', 1),
  ('21502', 'ANCASH', 'YUNGAY', 'CASCAPARA', 1),
  ('21503', 'ANCASH', 'YUNGAY', 'MANCOS', 1),
  ('21504', 'ANCASH', 'YUNGAY', 'MATACOTO', 1),
  ('21505', 'ANCASH', 'YUNGAY', 'QUILLO', 1),
  ('21506', 'ANCASH', 'YUNGAY', 'RANRAHIRCA', 1),
  ('21507', 'ANCASH', 'YUNGAY', 'SHUPLUY', 1),
  ('21508', 'ANCASH', 'YUNGAY', 'YANAMA', 1),
  (
    '21601',
    'ANCASH',
    'ANTONIO RAYMONDI',
    'LLAMELLIN',
    1
  ),
  ('21602', 'ANCASH', 'ANTONIO RAYMONDI', 'ACZO', 1),
  (
    '21603',
    'ANCASH',
    'ANTONIO RAYMONDI',
    'CHACCHO',
    1
  ),
  (
    '21604',
    'ANCASH',
    'ANTONIO RAYMONDI',
    'CHINGAS',
    1
  ),
  (
    '21605',
    'ANCASH',
    'ANTONIO RAYMONDI',
    'MIRGAS',
    1
  ),
  (
    '21606',
    'ANCASH',
    'ANTONIO RAYMONDI',
    'SAN JUAN DE RONTOY',
    1
  ),
  (
    '21701',
    'ANCASH',
    'CARLOS FERMIN FITZCARRALD',
    'SAN LUIS',
    1
  ),
  (
    '21702',
    'ANCASH',
    'CARLOS FERMIN FITZCARRALD',
    'YAUYA',
    1
  ),
  (
    '21703',
    'ANCASH',
    'CARLOS FERMIN FITZCARRALD',
    'SAN NICOLAS',
    1
  ),
  ('21801', 'ANCASH', 'ASUNCION', 'CHACAS', 1),
  ('21802', 'ANCASH', 'ASUNCION', 'ACOCHACA', 1),
  ('21901', 'ANCASH', 'HUARMEY', 'HUARMEY', 1),
  ('21902', 'ANCASH', 'HUARMEY', 'COCHAPETI', 1),
  ('21903', 'ANCASH', 'HUARMEY', 'HUAYAN', 1),
  ('21904', 'ANCASH', 'HUARMEY', 'MALVAS', 1),
  ('21905', 'ANCASH', 'HUARMEY', 'CULEBRAS', 1),
  ('22001', 'ANCASH', 'OCROS', 'ACAS', 1),
  ('22002', 'ANCASH', 'OCROS', 'CAJAMARQUILLA', 1),
  ('22003', 'ANCASH', 'OCROS', 'CARHUAPAMPA', 1),
  ('22004', 'ANCASH', 'OCROS', 'COCHAS', 1),
  ('22005', 'ANCASH', 'OCROS', 'CONGAS', 1),
  ('22006', 'ANCASH', 'OCROS', 'LLIPA', 1),
  ('22007', 'ANCASH', 'OCROS', 'OCROS', 1),
  (
    '22008',
    'ANCASH',
    'OCROS',
    'SAN CRISTOBAL DE RAJAN',
    1
  ),
  ('22009', 'ANCASH', 'OCROS', 'SAN PEDRO', 1),
  (
    '22010',
    'ANCASH',
    'OCROS',
    'SANTIAGO DE CHILCAS',
    1
  ),
  ('220101', 'TACNA', 'TACNA', 'TACNA', 1),
  ('220102', 'TACNA', 'TACNA', 'CALANA', 1),
  ('220104', 'TACNA', 'TACNA', 'INCLAN', 1),
  ('220107', 'TACNA', 'TACNA', 'PACHIA', 1),
  ('220108', 'TACNA', 'TACNA', 'PALCA', 1),
  ('220109', 'TACNA', 'TACNA', 'POCOLLAY', 1),
  ('220110', 'TACNA', 'TACNA', 'SAMA', 1),
  (
    '220111',
    'TACNA',
    'TACNA',
    'ALTO DE LA ALIANZA',
    1
  ),
  ('220112', 'TACNA', 'TACNA', 'CIUDAD NUEVA', 1),
  (
    '220113',
    'TACNA',
    'TACNA',
    'CORONEL GREGORIO ALBARRACIN LANCHIP',
    1
  ),
  (
    '220114',
    'TACNA',
    'TACNA',
    'LA YARADA LOS PALOS',
    1
  ),
  ('220201', 'TACNA', 'TARATA', 'TARATA', 1),
  ('220205', 'TACNA', 'TARATA', 'CHUCATAMANI', 1),
  ('220206', 'TACNA', 'TARATA', 'ESTIQUE', 1),
  ('220207', 'TACNA', 'TARATA', 'ESTIQUE-PAMPA', 1),
  ('220210', 'TACNA', 'TARATA', 'SITAJARA', 1),
  ('220211', 'TACNA', 'TARATA', 'SUSAPAYA', 1),
  ('220212', 'TACNA', 'TARATA', 'TARUCACHI', 1),
  ('220213', 'TACNA', 'TARATA', 'TICACO', 1),
  ('220301', 'TACNA', 'JORGE BASADRE', 'LOCUMBA', 1),
  ('220302', 'TACNA', 'JORGE BASADRE', 'ITE', 1),
  ('220303', 'TACNA', 'JORGE BASADRE', 'ILABAYA', 1),
  ('220401', 'TACNA', 'CANDARAVE', 'CANDARAVE', 1),
  ('220402', 'TACNA', 'CANDARAVE', 'CAIRANI', 1),
  ('220403', 'TACNA', 'CANDARAVE', 'CURIBAYA', 1),
  ('220404', 'TACNA', 'CANDARAVE', 'HUANUARA', 1),
  ('220405', 'TACNA', 'CANDARAVE', 'QUILAHUANI', 1),
  ('220406', 'TACNA', 'CANDARAVE', 'CAMILACA', 1),
  ('230101', 'TUMBES', 'TUMBES', 'TUMBES', 1),
  ('230102', 'TUMBES', 'TUMBES', 'CORRALES', 1),
  ('230103', 'TUMBES', 'TUMBES', 'LA CRUZ', 1),
  (
    '230104',
    'TUMBES',
    'TUMBES',
    'PAMPAS DE HOSPITAL',
    1
  ),
  ('230105', 'TUMBES', 'TUMBES', 'SAN JACINTO', 1),
  (
    '230106',
    'TUMBES',
    'TUMBES',
    'SAN JUAN DE LA VIRGEN',
    1
  ),
  (
    '230201',
    'TUMBES',
    'CONTRALMIRANTE VILLAR',
    'ZORRITOS',
    1
  ),
  (
    '230202',
    'TUMBES',
    'CONTRALMIRANTE VILLAR',
    'CASITAS',
    1
  ),
  (
    '230203',
    'TUMBES',
    'CONTRALMIRANTE VILLAR',
    'CANOAS DE PUNTA SAL',
    1
  ),
  ('230301', 'TUMBES', 'ZARUMILLA', 'ZARUMILLA', 1),
  ('230302', 'TUMBES', 'ZARUMILLA', 'MATAPALO', 1),
  ('230303', 'TUMBES', 'ZARUMILLA', 'PAPAYAL', 1),
  (
    '230304',
    'TUMBES',
    'ZARUMILLA',
    'AGUAS VERDES',
    1
  ),
  ('240101', 'CALLAO', 'CALLAO', 'CALLAO', 1),
  ('240102', 'CALLAO', 'CALLAO', 'BELLAVISTA', 1),
  ('240103', 'CALLAO', 'CALLAO', 'LA PUNTA', 1),
  (
    '240104',
    'CALLAO',
    'CALLAO',
    'CARMEN DE LA LEGUA REYNOSO',
    1
  ),
  ('240105', 'CALLAO', 'CALLAO', 'LA PERLA', 1),
  ('240106', 'CALLAO', 'CALLAO', 'VENTANILLA', 1),
  ('240107', 'CALLAO', 'CALLAO', 'MI PERU', 1),
  (
    '250101',
    'UCAYALI',
    'CORONEL PORTILLO',
    'CALLERIA',
    1
  ),
  (
    '250102',
    'UCAYALI',
    'CORONEL PORTILLO',
    'YARINACOCHA',
    1
  ),
  (
    '250103',
    'UCAYALI',
    'CORONEL PORTILLO',
    'MASISEA',
    1
  ),
  (
    '250104',
    'UCAYALI',
    'CORONEL PORTILLO',
    'CAMPOVERDE',
    1
  ),
  (
    '250105',
    'UCAYALI',
    'CORONEL PORTILLO',
    'IPARIA',
    1
  ),
  (
    '250106',
    'UCAYALI',
    'CORONEL PORTILLO',
    'NUEVA REQUENA',
    1
  ),
  (
    '250107',
    'UCAYALI',
    'CORONEL PORTILLO',
    'MANANTAY',
    1
  ),
  (
    '250201',
    'UCAYALI',
    'PADRE ABAD',
    'PADRE ABAD',
    1
  ),
  ('250202', 'UCAYALI', 'PADRE ABAD', 'IRAZOLA', 1),
  ('250203', 'UCAYALI', 'PADRE ABAD', 'CURIMANA', 1),
  ('250204', 'UCAYALI', 'PADRE ABAD', 'NESHUYA', 1),
  (
    '250205',
    'UCAYALI',
    'PADRE ABAD',
    'ALEXANDER VON HUMBOLDT',
    1
  ),
  ('250206', 'UCAYALI', 'PADRE ABAD', 'BOQUERON', 1),
  ('250207', 'UCAYALI', 'PADRE ABAD', 'HUIPOCA', 1),
  ('250301', 'UCAYALI', 'ATALAYA', 'RAYMONDI', 1),
  ('250302', 'UCAYALI', 'ATALAYA', 'TAHUANIA', 1),
  ('250303', 'UCAYALI', 'ATALAYA', 'YURUA', 1),
  ('250304', 'UCAYALI', 'ATALAYA', 'SEPAHUA', 1),
  ('250401', 'UCAYALI', 'PURUS', 'PURUS', 1),
  ('30101', 'APURIMAC', 'ABANCAY', 'ABANCAY', 1),
  ('30102', 'APURIMAC', 'ABANCAY', 'CIRCA', 1),
  ('30103', 'APURIMAC', 'ABANCAY', 'CURAHUASI', 1),
  ('30104', 'APURIMAC', 'ABANCAY', 'CHACOCHE', 1),
  ('30105', 'APURIMAC', 'ABANCAY', 'HUANIPACA', 1),
  ('30106', 'APURIMAC', 'ABANCAY', 'LAMBRAMA', 1),
  ('30107', 'APURIMAC', 'ABANCAY', 'PICHIRHUA', 1),
  (
    '30108',
    'APURIMAC',
    'ABANCAY',
    'SAN PEDRO DE CACHORA',
    1
  ),
  ('30109', 'APURIMAC', 'ABANCAY', 'TAMBURCO', 1),
  ('30201', 'APURIMAC', 'AYMARAES', 'CHALHUANCA', 1),
  ('30202', 'APURIMAC', 'AYMARAES', 'CAPAYA', 1),
  ('30203', 'APURIMAC', 'AYMARAES', 'CARAYBAMBA', 1),
  ('30204', 'APURIMAC', 'AYMARAES', 'COLCABAMBA', 1),
  ('30205', 'APURIMAC', 'AYMARAES', 'COTARUSE', 1),
  ('30206', 'APURIMAC', 'AYMARAES', 'CHAPIMARCA', 1),
  ('30207', 'APURIMAC', 'AYMARAES', 'HUAYLLO', 1),
  ('30208', 'APURIMAC', 'AYMARAES', 'LUCRE', 1),
  ('30209', 'APURIMAC', 'AYMARAES', 'POCOHUANCA', 1),
  ('30210', 'APURIMAC', 'AYMARAES', 'SAÑAYCA', 1),
  ('30211', 'APURIMAC', 'AYMARAES', 'SORAYA', 1),
  ('30212', 'APURIMAC', 'AYMARAES', 'TAPAIRIHUA', 1),
  ('30213', 'APURIMAC', 'AYMARAES', 'TINTAY', 1),
  ('30214', 'APURIMAC', 'AYMARAES', 'TORAYA', 1),
  ('30215', 'APURIMAC', 'AYMARAES', 'YANACA', 1),
  (
    '30216',
    'APURIMAC',
    'AYMARAES',
    'SAN JUAN DE CHACÑA',
    1
  ),
  (
    '30217',
    'APURIMAC',
    'AYMARAES',
    'JUSTO APU SAHUARAURA',
    1
  ),
  (
    '30301',
    'APURIMAC',
    'ANDAHUAYLAS',
    'ANDAHUAYLAS',
    1
  ),
  (
    '30302',
    'APURIMAC',
    'ANDAHUAYLAS',
    'ANDARAPA',
    1
  ),
  ('30303', 'APURIMAC', 'ANDAHUAYLAS', 'CHIARA', 1),
  (
    '30304',
    'APURIMAC',
    'ANDAHUAYLAS',
    'HUANCARAMA',
    1
  ),
  (
    '30305',
    'APURIMAC',
    'ANDAHUAYLAS',
    'HUANCARAY',
    1
  ),
  (
    '30306',
    'APURIMAC',
    'ANDAHUAYLAS',
    'KISHUARA',
    1
  ),
  (
    '30307',
    'APURIMAC',
    'ANDAHUAYLAS',
    'PACOBAMBA',
    1
  ),
  (
    '30308',
    'APURIMAC',
    'ANDAHUAYLAS',
    'PAMPACHIRI',
    1
  ),
  (
    '30309',
    'APURIMAC',
    'ANDAHUAYLAS',
    'SAN ANTONIO DE CACHI',
    1
  ),
  (
    '30310',
    'APURIMAC',
    'ANDAHUAYLAS',
    'SAN JERONIMO',
    1
  ),
  (
    '30311',
    'APURIMAC',
    'ANDAHUAYLAS',
    'TALAVERA',
    1
  ),
  ('30312', 'APURIMAC', 'ANDAHUAYLAS', 'TURPO', 1),
  ('30313', 'APURIMAC', 'ANDAHUAYLAS', 'PACUCHA', 1),
  (
    '30314',
    'APURIMAC',
    'ANDAHUAYLAS',
    'POMACOCHA',
    1
  ),
  (
    '30315',
    'APURIMAC',
    'ANDAHUAYLAS',
    'SANTA MARIA DE CHICMO',
    1
  ),
  (
    '30316',
    'APURIMAC',
    'ANDAHUAYLAS',
    'TUMAY HUARACA',
    1
  ),
  ('30317', 'APURIMAC', 'ANDAHUAYLAS', 'HUAYANA', 1),
  (
    '30318',
    'APURIMAC',
    'ANDAHUAYLAS',
    'SAN MIGUEL DE CHACCRAMPA',
    1
  ),
  (
    '30319',
    'APURIMAC',
    'ANDAHUAYLAS',
    'KAQUIABAMBA',
    1
  ),
  (
    '30320',
    'APURIMAC',
    'ANDAHUAYLAS',
    'JOSE MARIA ARGUEDAS',
    1
  ),
  ('30401', 'APURIMAC', 'ANTABAMBA', 'ANTABAMBA', 1),
  ('30402', 'APURIMAC', 'ANTABAMBA', 'EL ORO', 1),
  ('30403', 'APURIMAC', 'ANTABAMBA', 'HUAQUIRCA', 1),
  (
    '30404',
    'APURIMAC',
    'ANTABAMBA',
    'JUAN ESPINOZA MEDRANO',
    1
  ),
  ('30405', 'APURIMAC', 'ANTABAMBA', 'OROPESA', 1),
  (
    '30406',
    'APURIMAC',
    'ANTABAMBA',
    'PACHACONAS',
    1
  ),
  ('30407', 'APURIMAC', 'ANTABAMBA', 'SABAINO', 1),
  (
    '30501',
    'APURIMAC',
    'COTABAMBAS',
    'TAMBOBAMBA',
    1
  ),
  (
    '30502',
    'APURIMAC',
    'COTABAMBAS',
    'COYLLURQUI',
    1
  ),
  (
    '30503',
    'APURIMAC',
    'COTABAMBAS',
    'COTABAMBAS',
    1
  ),
  ('30504', 'APURIMAC', 'COTABAMBAS', 'HAQUIRA', 1),
  ('30505', 'APURIMAC', 'COTABAMBAS', 'MARA', 1),
  (
    '30506',
    'APURIMAC',
    'COTABAMBAS',
    'CHALLHUAHUACHO',
    1
  ),
  ('30601', 'APURIMAC', 'GRAU', 'CHUQUIBAMBILLA', 1),
  ('30602', 'APURIMAC', 'GRAU', 'CURPAHUASI', 1),
  ('30603', 'APURIMAC', 'GRAU', 'HUAYLLATI', 1),
  ('30604', 'APURIMAC', 'GRAU', 'MAMARA', 1),
  ('30605', 'APURIMAC', 'GRAU', 'GAMARRA', 1),
  (
    '30606',
    'APURIMAC',
    'GRAU',
    'MICAELA BASTIDAS',
    1
  ),
  ('30607', 'APURIMAC', 'GRAU', 'PROGRESO', 1),
  ('30608', 'APURIMAC', 'GRAU', 'PATAYPAMPA', 1),
  ('30609', 'APURIMAC', 'GRAU', 'SAN ANTONIO', 1),
  ('30610', 'APURIMAC', 'GRAU', 'TURPAY', 1),
  ('30611', 'APURIMAC', 'GRAU', 'VILCABAMBA', 1),
  ('30612', 'APURIMAC', 'GRAU', 'VIRUNDO', 1),
  ('30613', 'APURIMAC', 'GRAU', 'SANTA ROSA', 1),
  ('30614', 'APURIMAC', 'GRAU', 'CURASCO', 1),
  (
    '30701',
    'APURIMAC',
    'CHINCHEROS',
    'CHINCHEROS',
    1
  ),
  ('30702', 'APURIMAC', 'CHINCHEROS', 'ONGOY', 1),
  ('30703', 'APURIMAC', 'CHINCHEROS', 'OCOBAMBA', 1),
  (
    '30704',
    'APURIMAC',
    'CHINCHEROS',
    'COCHARCAS',
    1
  ),
  (
    '30705',
    'APURIMAC',
    'CHINCHEROS',
    'ANCO-HUALLO',
    1
  ),
  ('30706', 'APURIMAC', 'CHINCHEROS', 'HUACCANA', 1),
  (
    '30707',
    'APURIMAC',
    'CHINCHEROS',
    'URANMARCA',
    1
  ),
  (
    '30708',
    'APURIMAC',
    'CHINCHEROS',
    'RANRACANCHA',
    1
  ),
  ('30709', 'APURIMAC', 'CHINCHEROS', 'ROCCHACC', 1),
  (
    '30710',
    'APURIMAC',
    'CHINCHEROS',
    'EL PORVENIR',
    1
  ),
  (
    '30711',
    'APURIMAC',
    'CHINCHEROS',
    'LOS CHANKAS',
    1
  ),
  ('30712', 'APURIMAC', 'CHINCHEROS', 'AHUAYRO', 1),
  ('40101', 'AREQUIPA', 'AREQUIPA', 'AREQUIPA', 1),
  ('40102', 'AREQUIPA', 'AREQUIPA', 'CAYMA', 1),
  (
    '40103',
    'AREQUIPA',
    'AREQUIPA',
    'CERRO COLORADO',
    1
  ),
  ('40104', 'AREQUIPA', 'AREQUIPA', 'CHARACATO', 1),
  ('40105', 'AREQUIPA', 'AREQUIPA', 'CHIGUATA', 1),
  ('40106', 'AREQUIPA', 'AREQUIPA', 'LA JOYA', 1),
  ('40107', 'AREQUIPA', 'AREQUIPA', 'MIRAFLORES', 1),
  ('40108', 'AREQUIPA', 'AREQUIPA', 'MOLLEBAYA', 1),
  ('40109', 'AREQUIPA', 'AREQUIPA', 'PAUCARPATA', 1),
  ('40110', 'AREQUIPA', 'AREQUIPA', 'POCSI', 1),
  ('40111', 'AREQUIPA', 'AREQUIPA', 'POLOBAYA', 1),
  ('40112', 'AREQUIPA', 'AREQUIPA', 'QUEQUEÑA', 1),
  ('40113', 'AREQUIPA', 'AREQUIPA', 'SABANDIA', 1),
  ('40114', 'AREQUIPA', 'AREQUIPA', 'SACHACA', 1),
  (
    '40115',
    'AREQUIPA',
    'AREQUIPA',
    'SAN JUAN DE SIGUAS',
    1
  ),
  (
    '40116',
    'AREQUIPA',
    'AREQUIPA',
    'SAN JUAN DE TARUCANI',
    1
  ),
  (
    '40117',
    'AREQUIPA',
    'AREQUIPA',
    'SANTA ISABEL DE SIGUAS',
    1
  ),
  (
    '40118',
    'AREQUIPA',
    'AREQUIPA',
    'SANTA RITA DE SIGUAS',
    1
  ),
  ('40119', 'AREQUIPA', 'AREQUIPA', 'SOCABAYA', 1),
  ('40120', 'AREQUIPA', 'AREQUIPA', 'TIABAYA', 1),
  ('40121', 'AREQUIPA', 'AREQUIPA', 'UCHUMAYO', 1),
  ('40122', 'AREQUIPA', 'AREQUIPA', 'VITOR', 1),
  ('40123', 'AREQUIPA', 'AREQUIPA', 'YANAHUARA', 1),
  ('40124', 'AREQUIPA', 'AREQUIPA', 'YARABAMBA', 1),
  ('40125', 'AREQUIPA', 'AREQUIPA', 'YURA', 1),
  (
    '40126',
    'AREQUIPA',
    'AREQUIPA',
    'MARIANO MELGAR',
    1
  ),
  (
    '40127',
    'AREQUIPA',
    'AREQUIPA',
    'JACOBO HUNTER',
    1
  ),
  (
    '40128',
    'AREQUIPA',
    'AREQUIPA',
    'ALTO SELVA ALEGRE',
    1
  ),
  (
    '40129',
    'AREQUIPA',
    'AREQUIPA',
    'JOSE LUIS BUSTAMANTE Y RIVERO',
    1
  ),
  ('40201', 'AREQUIPA', 'CAYLLOMA', 'CHIVAY', 1),
  ('40202', 'AREQUIPA', 'CAYLLOMA', 'ACHOMA', 1),
  (
    '40203',
    'AREQUIPA',
    'CAYLLOMA',
    'CABANACONDE',
    1
  ),
  ('40204', 'AREQUIPA', 'CAYLLOMA', 'CAYLLOMA', 1),
  ('40205', 'AREQUIPA', 'CAYLLOMA', 'CALLALLI', 1),
  ('40206', 'AREQUIPA', 'CAYLLOMA', 'COPORAQUE', 1),
  ('40207', 'AREQUIPA', 'CAYLLOMA', 'HUAMBO', 1),
  ('40208', 'AREQUIPA', 'CAYLLOMA', 'HUANCA', 1),
  ('40209', 'AREQUIPA', 'CAYLLOMA', 'ICHUPAMPA', 1),
  ('40210', 'AREQUIPA', 'CAYLLOMA', 'LARI', 1),
  ('40211', 'AREQUIPA', 'CAYLLOMA', 'LLUTA', 1),
  ('40212', 'AREQUIPA', 'CAYLLOMA', 'MACA', 1),
  ('40213', 'AREQUIPA', 'CAYLLOMA', 'MADRIGAL', 1),
  (
    '40214',
    'AREQUIPA',
    'CAYLLOMA',
    'SAN ANTONIO DE CHUCA',
    1
  ),
  ('40215', 'AREQUIPA', 'CAYLLOMA', 'SIBAYO', 1),
  ('40216', 'AREQUIPA', 'CAYLLOMA', 'TAPAY', 1),
  ('40217', 'AREQUIPA', 'CAYLLOMA', 'TISCO', 1),
  ('40218', 'AREQUIPA', 'CAYLLOMA', 'TUTI', 1),
  ('40219', 'AREQUIPA', 'CAYLLOMA', 'YANQUE', 1),
  ('40220', 'AREQUIPA', 'CAYLLOMA', 'MAJES', 1),
  ('40301', 'AREQUIPA', 'CAMANA', 'CAMANA', 1),
  (
    '40302',
    'AREQUIPA',
    'CAMANA',
    'JOSE MARIA QUIMPER',
    1
  ),
  (
    '40303',
    'AREQUIPA',
    'CAMANA',
    'MARIANO NICOLAS VALCARCEL',
    1
  ),
  (
    '40304',
    'AREQUIPA',
    'CAMANA',
    'MARISCAL CACERES',
    1
  ),
  (
    '40305',
    'AREQUIPA',
    'CAMANA',
    'NICOLAS DE PIEROLA',
    1
  ),
  ('40306', 'AREQUIPA', 'CAMANA', 'OCOÑA', 1),
  ('40307', 'AREQUIPA', 'CAMANA', 'QUILCA', 1),
  (
    '40308',
    'AREQUIPA',
    'CAMANA',
    'SAMUEL PASTOR',
    1
  ),
  ('40401', 'AREQUIPA', 'CARAVELI', 'CARAVELI', 1),
  ('40402', 'AREQUIPA', 'CARAVELI', 'ACARI', 1),
  ('40403', 'AREQUIPA', 'CARAVELI', 'ATICO', 1),
  ('40404', 'AREQUIPA', 'CARAVELI', 'ATIQUIPA', 1),
  (
    '40405',
    'AREQUIPA',
    'CARAVELI',
    'BELLA UNION',
    1
  ),
  ('40406', 'AREQUIPA', 'CARAVELI', 'CAHUACHO', 1),
  ('40407', 'AREQUIPA', 'CARAVELI', 'CHALA', 1),
  ('40408', 'AREQUIPA', 'CARAVELI', 'CHAPARRA', 1),
  ('40409', 'AREQUIPA', 'CARAVELI', 'HUANUHUANU', 1),
  ('40410', 'AREQUIPA', 'CARAVELI', 'JAQUI', 1),
  ('40411', 'AREQUIPA', 'CARAVELI', 'LOMAS', 1),
  ('40412', 'AREQUIPA', 'CARAVELI', 'QUICACHA', 1),
  ('40413', 'AREQUIPA', 'CARAVELI', 'YAUCA', 1),
  ('40501', 'AREQUIPA', 'CASTILLA', 'APLAO', 1),
  ('40502', 'AREQUIPA', 'CASTILLA', 'ANDAGUA', 1),
  ('40503', 'AREQUIPA', 'CASTILLA', 'AYO', 1),
  ('40504', 'AREQUIPA', 'CASTILLA', 'CHACHAS', 1),
  (
    '40505',
    'AREQUIPA',
    'CASTILLA',
    'CHILCAYMARCA',
    1
  ),
  ('40506', 'AREQUIPA', 'CASTILLA', 'CHOCO', 1),
  ('40507', 'AREQUIPA', 'CASTILLA', 'HUANCARQUI', 1),
  ('40508', 'AREQUIPA', 'CASTILLA', 'MACHAGUAY', 1),
  ('40509', 'AREQUIPA', 'CASTILLA', 'ORCOPAMPA', 1),
  ('40510', 'AREQUIPA', 'CASTILLA', 'PAMPACOLCA', 1),
  ('40511', 'AREQUIPA', 'CASTILLA', 'TIPAN', 1),
  ('40512', 'AREQUIPA', 'CASTILLA', 'URACA', 1),
  ('40513', 'AREQUIPA', 'CASTILLA', 'UÑON', 1),
  ('40514', 'AREQUIPA', 'CASTILLA', 'VIRACO', 1),
  (
    '40601',
    'AREQUIPA',
    'CONDESUYOS',
    'CHUQUIBAMBA',
    1
  ),
  ('40602', 'AREQUIPA', 'CONDESUYOS', 'ANDARAY', 1),
  ('40603', 'AREQUIPA', 'CONDESUYOS', 'CAYARANI', 1),
  ('40604', 'AREQUIPA', 'CONDESUYOS', 'CHICHAS', 1),
  ('40605', 'AREQUIPA', 'CONDESUYOS', 'IRAY', 1),
  (
    '40606',
    'AREQUIPA',
    'CONDESUYOS',
    'SALAMANCA',
    1
  ),
  (
    '40607',
    'AREQUIPA',
    'CONDESUYOS',
    'YANAQUIHUA',
    1
  ),
  (
    '40608',
    'AREQUIPA',
    'CONDESUYOS',
    'RIO GRANDE',
    1
  ),
  ('40701', 'AREQUIPA', 'ISLAY', 'MOLLENDO', 1),
  ('40702', 'AREQUIPA', 'ISLAY', 'COCACHACRA', 1),
  ('40703', 'AREQUIPA', 'ISLAY', 'DEAN VALDIVIA', 1),
  ('40704', 'AREQUIPA', 'ISLAY', 'ISLAY', 1),
  ('40705', 'AREQUIPA', 'ISLAY', 'MEJIA', 1),
  (
    '40706',
    'AREQUIPA',
    'ISLAY',
    'PUNTA DE BOMBON',
    1
  ),
  ('40801', 'AREQUIPA', 'LA UNION', 'COTAHUASI', 1),
  ('40802', 'AREQUIPA', 'LA UNION', 'ALCA', 1),
  ('40803', 'AREQUIPA', 'LA UNION', 'CHARCANA', 1),
  (
    '40804',
    'AREQUIPA',
    'LA UNION',
    'HUAYNACOTAS',
    1
  ),
  ('40805', 'AREQUIPA', 'LA UNION', 'PAMPAMARCA', 1),
  ('40806', 'AREQUIPA', 'LA UNION', 'PUYCA', 1),
  ('40807', 'AREQUIPA', 'LA UNION', 'QUECHUALLA', 1),
  ('40808', 'AREQUIPA', 'LA UNION', 'SAYLA', 1),
  ('40809', 'AREQUIPA', 'LA UNION', 'TAURIA', 1),
  ('40810', 'AREQUIPA', 'LA UNION', 'TOMEPAMPA', 1),
  ('40811', 'AREQUIPA', 'LA UNION', 'TORO', 1),
  ('50101', 'AYACUCHO', 'HUAMANGA', 'AYACUCHO', 1),
  (
    '50102',
    'AYACUCHO',
    'HUAMANGA',
    'ACOS VINCHOS',
    1
  ),
  (
    '50103',
    'AYACUCHO',
    'HUAMANGA',
    'CARMEN ALTO',
    1
  ),
  ('50104', 'AYACUCHO', 'HUAMANGA', 'CHIARA', 1),
  ('50105', 'AYACUCHO', 'HUAMANGA', 'QUINUA', 1),
  (
    '50106',
    'AYACUCHO',
    'HUAMANGA',
    'SAN JOSE DE TICLLAS',
    1
  ),
  (
    '50107',
    'AYACUCHO',
    'HUAMANGA',
    'SAN JUAN BAUTISTA',
    1
  ),
  (
    '50108',
    'AYACUCHO',
    'HUAMANGA',
    'SANTIAGO DE PISCHA',
    1
  ),
  ('50109', 'AYACUCHO', 'HUAMANGA', 'VINCHOS', 1),
  ('50110', 'AYACUCHO', 'HUAMANGA', 'TAMBILLO', 1),
  ('50111', 'AYACUCHO', 'HUAMANGA', 'ACOCRO', 1),
  ('50112', 'AYACUCHO', 'HUAMANGA', 'SOCOS', 1),
  ('50113', 'AYACUCHO', 'HUAMANGA', 'OCROS', 1),
  ('50114', 'AYACUCHO', 'HUAMANGA', 'PACAYCASA', 1),
  (
    '50115',
    'AYACUCHO',
    'HUAMANGA',
    'JESUS NAZARENO',
    1
  ),
  (
    '50116',
    'AYACUCHO',
    'HUAMANGA',
    'ANDRES AVELINO CACERES DORREGARAY',
    1
  ),
  ('50201', 'AYACUCHO', 'CANGALLO', 'CANGALLO', 1),
  ('50204', 'AYACUCHO', 'CANGALLO', 'CHUSCHI', 1),
  (
    '50206',
    'AYACUCHO',
    'CANGALLO',
    'LOS MOROCHUCOS',
    1
  ),
  ('50207', 'AYACUCHO', 'CANGALLO', 'PARAS', 1),
  ('50208', 'AYACUCHO', 'CANGALLO', 'TOTOS', 1),
  (
    '50211',
    'AYACUCHO',
    'CANGALLO',
    'MARIA PARADO DE BELLIDO',
    1
  ),
  ('50301', 'AYACUCHO', 'HUANTA', 'HUANTA', 1),
  ('50302', 'AYACUCHO', 'HUANTA', 'AYAHUANCO', 1),
  ('50303', 'AYACUCHO', 'HUANTA', 'HUAMANGUILLA', 1),
  ('50304', 'AYACUCHO', 'HUANTA', 'IGUAIN', 1),
  ('50305', 'AYACUCHO', 'HUANTA', 'LURICOCHA', 1),
  ('50307', 'AYACUCHO', 'HUANTA', 'SANTILLANA', 1),
  ('50308', 'AYACUCHO', 'HUANTA', 'SIVIA', 1),
  ('50309', 'AYACUCHO', 'HUANTA', 'LLOCHEGUA', 1),
  ('50310', 'AYACUCHO', 'HUANTA', 'CANAYRE', 1),
  ('50311', 'AYACUCHO', 'HUANTA', 'UCHURACCAY', 1),
  ('50312', 'AYACUCHO', 'HUANTA', 'PUCACOLPA', 1),
  ('50313', 'AYACUCHO', 'HUANTA', 'CHACA', 1),
  ('50314', 'AYACUCHO', 'HUANTA', 'PUTIS', 1),
  ('50401', 'AYACUCHO', 'LA MAR', 'SAN MIGUEL', 1),
  ('50402', 'AYACUCHO', 'LA MAR', 'ANCO', 1),
  ('50403', 'AYACUCHO', 'LA MAR', 'AYNA', 1),
  ('50404', 'AYACUCHO', 'LA MAR', 'CHILCAS', 1),
  ('50405', 'AYACUCHO', 'LA MAR', 'CHUNGUI', 1),
  ('50406', 'AYACUCHO', 'LA MAR', 'TAMBO', 1),
  (
    '50407',
    'AYACUCHO',
    'LA MAR',
    'LUIS CARRANZA',
    1
  ),
  ('50408', 'AYACUCHO', 'LA MAR', 'SANTA ROSA', 1),
  ('50409', 'AYACUCHO', 'LA MAR', 'SAMUGARI', 1),
  ('50410', 'AYACUCHO', 'LA MAR', 'ANCHIHUAY', 1),
  ('50411', 'AYACUCHO', 'LA MAR', 'ORONCCOY', 1),
  (
    '50412',
    'AYACUCHO',
    'LA MAR',
    'UNION PROGRESO',
    1
  ),
  ('50413', 'AYACUCHO', 'LA MAR', 'PATIBAMBA', 1),
  ('50414', 'AYACUCHO', 'LA MAR', 'NINABAMBA', 1),
  (
    '50415',
    'AYACUCHO',
    'LA MAR',
    'RIO MAGDALENA',
    1
  ),
  ('50501', 'AYACUCHO', 'LUCANAS', 'PUQUIO', 1),
  ('50502', 'AYACUCHO', 'LUCANAS', 'AUCARA', 1),
  ('50503', 'AYACUCHO', 'LUCANAS', 'CABANA', 1),
  (
    '50504',
    'AYACUCHO',
    'LUCANAS',
    'CARMEN SALCEDO',
    1
  ),
  ('50506', 'AYACUCHO', 'LUCANAS', 'CHAVIÑA', 1),
  ('50508', 'AYACUCHO', 'LUCANAS', 'CHIPAO', 1),
  ('50510', 'AYACUCHO', 'LUCANAS', 'HUAC-HUAS', 1),
  ('50511', 'AYACUCHO', 'LUCANAS', 'LARAMATE', 1),
  (
    '50512',
    'AYACUCHO',
    'LUCANAS',
    'LEONCIO PRADO',
    1
  ),
  ('50513', 'AYACUCHO', 'LUCANAS', 'LUCANAS', 1),
  ('50514', 'AYACUCHO', 'LUCANAS', 'LLAUTA', 1),
  ('50516', 'AYACUCHO', 'LUCANAS', 'OCAÑA', 1),
  ('50517', 'AYACUCHO', 'LUCANAS', 'OTOCA', 1),
  ('50520', 'AYACUCHO', 'LUCANAS', 'SANCOS', 1),
  ('50521', 'AYACUCHO', 'LUCANAS', 'SAN JUAN', 1),
  ('50522', 'AYACUCHO', 'LUCANAS', 'SAN PEDRO', 1),
  (
    '50524',
    'AYACUCHO',
    'LUCANAS',
    'SANTA ANA DE HUAYCAHUACHO',
    1
  ),
  ('50525', 'AYACUCHO', 'LUCANAS', 'SANTA LUCIA', 1),
  ('50529', 'AYACUCHO', 'LUCANAS', 'SAISA', 1),
  (
    '50531',
    'AYACUCHO',
    'LUCANAS',
    'SAN PEDRO DE PALCO',
    1
  ),
  (
    '50532',
    'AYACUCHO',
    'LUCANAS',
    'SAN CRISTOBAL',
    1
  ),
  (
    '50601',
    'AYACUCHO',
    'PARINACOCHAS',
    'CORACORA',
    1
  ),
  (
    '50604',
    'AYACUCHO',
    'PARINACOCHAS',
    'CORONEL CASTAÑEDA',
    1
  ),
  ('50605', 'AYACUCHO', 'PARINACOCHAS', 'CHUMPI', 1),
  (
    '50608',
    'AYACUCHO',
    'PARINACOCHAS',
    'PACAPAUSA',
    1
  ),
  ('50611', 'AYACUCHO', 'PARINACOCHAS', 'PULLO', 1),
  (
    '50612',
    'AYACUCHO',
    'PARINACOCHAS',
    'PUYUSCA',
    1
  ),
  (
    '50615',
    'AYACUCHO',
    'PARINACOCHAS',
    'SAN FRANCISCO DE RAVACAYCO',
    1
  ),
  (
    '50616',
    'AYACUCHO',
    'PARINACOCHAS',
    'UPAHUACHO',
    1
  ),
  (
    '50701',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'HUANCAPI',
    1
  ),
  (
    '50702',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'ALCAMENCA',
    1
  ),
  (
    '50703',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'APONGO',
    1
  ),
  (
    '50704',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'CANARIA',
    1
  ),
  (
    '50706',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'CAYARA',
    1
  ),
  (
    '50707',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'COLCA',
    1
  ),
  (
    '50708',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'HUAYA',
    1
  ),
  (
    '50709',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'HUAMANQUIQUIA',
    1
  ),
  (
    '50710',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'HUANCARAYLLA',
    1
  ),
  (
    '50713',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'SARHUA',
    1
  ),
  (
    '50714',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'VILCANCHOS',
    1
  ),
  (
    '50715',
    'AYACUCHO',
    'VICTOR FAJARDO',
    'ASQUIPATA',
    1
  ),
  (
    '50801',
    'AYACUCHO',
    'HUANCA SANCOS',
    'SANCOS',
    1
  ),
  (
    '50802',
    'AYACUCHO',
    'HUANCA SANCOS',
    'SACSAMARCA',
    1
  ),
  (
    '50803',
    'AYACUCHO',
    'HUANCA SANCOS',
    'SANTIAGO DE LUCANAMARCA',
    1
  ),
  (
    '50804',
    'AYACUCHO',
    'HUANCA SANCOS',
    'CARAPO',
    1
  ),
  (
    '50901',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'VILCAS HUAMAN',
    1
  ),
  (
    '50902',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'VISCHONGO',
    1
  ),
  (
    '50903',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'ACCOMARCA',
    1
  ),
  (
    '50904',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'CARHUANCA',
    1
  ),
  (
    '50905',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'CONCEPCION',
    1
  ),
  (
    '50906',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'HUAMBALPA',
    1
  ),
  (
    '50907',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'SAURAMA',
    1
  ),
  (
    '50908',
    'AYACUCHO',
    'VILCAS HUAMAN',
    'INDEPENDENCIA',
    1
  ),
  (
    '51001',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'PAUSA',
    1
  ),
  (
    '51002',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'COLTA',
    1
  ),
  (
    '51003',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'CORCULLA',
    1
  ),
  (
    '51004',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'LAMPA',
    1
  ),
  (
    '51005',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'MARCABAMBA',
    1
  ),
  (
    '51006',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'OYOLO',
    1
  ),
  (
    '51007',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'PARARCA',
    1
  ),
  (
    '51008',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'SAN JAVIER DE ALPABAMBA',
    1
  ),
  (
    '51009',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'SAN JOSE DE USHUA',
    1
  ),
  (
    '51010',
    'AYACUCHO',
    'PAUCAR DEL SARA SARA',
    'SARA SARA',
    1
  ),
  ('51101', 'AYACUCHO', 'SUCRE', 'QUEROBAMBA', 1),
  ('51102', 'AYACUCHO', 'SUCRE', 'BELEN', 1),
  ('51103', 'AYACUCHO', 'SUCRE', 'CHALCOS', 1),
  (
    '51104',
    'AYACUCHO',
    'SUCRE',
    'SAN SALVADOR DE QUIJE',
    1
  ),
  ('51105', 'AYACUCHO', 'SUCRE', 'PAICO', 1),
  (
    '51106',
    'AYACUCHO',
    'SUCRE',
    'SANTIAGO DE PAUCARAY',
    1
  ),
  (
    '51107',
    'AYACUCHO',
    'SUCRE',
    'SAN PEDRO DE LARCAY',
    1
  ),
  ('51108', 'AYACUCHO', 'SUCRE', 'SORAS', 1),
  ('51109', 'AYACUCHO', 'SUCRE', 'HUACAÑA', 1),
  ('51110', 'AYACUCHO', 'SUCRE', 'CHILCAYOC', 1),
  ('51111', 'AYACUCHO', 'SUCRE', 'MORCOLLA', 1),
  (
    '60101',
    'CAJAMARCA',
    'CAJAMARCA',
    'CAJAMARCA',
    1
  ),
  ('60102', 'CAJAMARCA', 'CAJAMARCA', 'ASUNCION', 1),
  ('60103', 'CAJAMARCA', 'CAJAMARCA', 'COSPAN', 1),
  ('60104', 'CAJAMARCA', 'CAJAMARCA', 'CHETILLA', 1),
  ('60105', 'CAJAMARCA', 'CAJAMARCA', 'ENCAÑADA', 1),
  ('60106', 'CAJAMARCA', 'CAJAMARCA', 'JESUS', 1),
  (
    '60107',
    'CAJAMARCA',
    'CAJAMARCA',
    'LOS BAÑOS DEL INCA',
    1
  ),
  (
    '60108',
    'CAJAMARCA',
    'CAJAMARCA',
    'LLACANORA',
    1
  ),
  (
    '60109',
    'CAJAMARCA',
    'CAJAMARCA',
    'MAGDALENA',
    1
  ),
  ('60110', 'CAJAMARCA', 'CAJAMARCA', 'MATARA', 1),
  ('60111', 'CAJAMARCA', 'CAJAMARCA', 'NAMORA', 1),
  ('60112', 'CAJAMARCA', 'CAJAMARCA', 'SAN JUAN', 1),
  (
    '60201',
    'CAJAMARCA',
    'CAJABAMBA',
    'CAJABAMBA',
    1
  ),
  ('60202', 'CAJAMARCA', 'CAJABAMBA', 'CACHACHI', 1),
  (
    '60203',
    'CAJAMARCA',
    'CAJABAMBA',
    'CONDEBAMBA',
    1
  ),
  (
    '60205',
    'CAJAMARCA',
    'CAJABAMBA',
    'SITACOCHA',
    1
  ),
  ('60301', 'CAJAMARCA', 'CELENDIN', 'CELENDIN', 1),
  ('60302', 'CAJAMARCA', 'CELENDIN', 'CORTEGANA', 1),
  ('60303', 'CAJAMARCA', 'CELENDIN', 'CHUMUCH', 1),
  ('60304', 'CAJAMARCA', 'CELENDIN', 'HUASMIN', 1),
  (
    '60305',
    'CAJAMARCA',
    'CELENDIN',
    'JORGE CHAVEZ',
    1
  ),
  (
    '60306',
    'CAJAMARCA',
    'CELENDIN',
    'JOSE GALVEZ',
    1
  ),
  (
    '60307',
    'CAJAMARCA',
    'CELENDIN',
    'MIGUEL IGLESIAS',
    1
  ),
  ('60308', 'CAJAMARCA', 'CELENDIN', 'OXAMARCA', 1),
  ('60309', 'CAJAMARCA', 'CELENDIN', 'SOROCHUCO', 1),
  ('60310', 'CAJAMARCA', 'CELENDIN', 'SUCRE', 1),
  ('60311', 'CAJAMARCA', 'CELENDIN', 'UTCO', 1),
  (
    '60312',
    'CAJAMARCA',
    'CELENDIN',
    'LA LIBERTAD DE PALLAN',
    1
  ),
  (
    '60401',
    'CAJAMARCA',
    'CONTUMAZA',
    'CONTUMAZA',
    1
  ),
  ('60403', 'CAJAMARCA', 'CONTUMAZA', 'CHILETE', 1),
  ('60404', 'CAJAMARCA', 'CONTUMAZA', 'GUZMANGO', 1),
  (
    '60405',
    'CAJAMARCA',
    'CONTUMAZA',
    'SAN BENITO',
    1
  ),
  (
    '60406',
    'CAJAMARCA',
    'CONTUMAZA',
    'CUPISNIQUE',
    1
  ),
  (
    '60407',
    'CAJAMARCA',
    'CONTUMAZA',
    'TANTARICA',
    1
  ),
  ('60408', 'CAJAMARCA', 'CONTUMAZA', 'YONAN', 1),
  (
    '60409',
    'CAJAMARCA',
    'CONTUMAZA',
    'SANTA CRUZ DE TOLEDO',
    1
  ),
  ('60501', 'CAJAMARCA', 'CUTERVO', 'CUTERVO', 1),
  ('60502', 'CAJAMARCA', 'CUTERVO', 'CALLAYUC', 1),
  ('60503', 'CAJAMARCA', 'CUTERVO', 'CUJILLO', 1),
  ('60504', 'CAJAMARCA', 'CUTERVO', 'CHOROS', 1),
  ('60505', 'CAJAMARCA', 'CUTERVO', 'LA RAMADA', 1),
  ('60506', 'CAJAMARCA', 'CUTERVO', 'PIMPINGOS', 1),
  (
    '60507',
    'CAJAMARCA',
    'CUTERVO',
    'QUEROCOTILLO',
    1
  ),
  (
    '60508',
    'CAJAMARCA',
    'CUTERVO',
    'SAN ANDRES DE CUTERVO',
    1
  ),
  (
    '60509',
    'CAJAMARCA',
    'CUTERVO',
    'SAN JUAN DE CUTERVO',
    1
  ),
  (
    '60510',
    'CAJAMARCA',
    'CUTERVO',
    'SAN LUIS DE LUCMA',
    1
  ),
  ('60511', 'CAJAMARCA', 'CUTERVO', 'SANTA CRUZ', 1),
  (
    '60512',
    'CAJAMARCA',
    'CUTERVO',
    'SANTO DOMINGO DE LA CAPILLA',
    1
  ),
  (
    '60513',
    'CAJAMARCA',
    'CUTERVO',
    'SANTO TOMAS',
    1
  ),
  ('60514', 'CAJAMARCA', 'CUTERVO', 'SOCOTA', 1),
  (
    '60515',
    'CAJAMARCA',
    'CUTERVO',
    'TORIBIO CASANOVA',
    1
  ),
  ('60601', 'CAJAMARCA', 'CHOTA', 'CHOTA', 1),
  ('60602', 'CAJAMARCA', 'CHOTA', 'ANGUIA', 1),
  ('60603', 'CAJAMARCA', 'CHOTA', 'COCHABAMBA', 1),
  ('60604', 'CAJAMARCA', 'CHOTA', 'CONCHAN', 1),
  ('60605', 'CAJAMARCA', 'CHOTA', 'CHADIN', 1),
  ('60606', 'CAJAMARCA', 'CHOTA', 'CHIGUIRIP', 1),
  ('60607', 'CAJAMARCA', 'CHOTA', 'CHIMBAN', 1),
  ('60608', 'CAJAMARCA', 'CHOTA', 'HUAMBOS', 1),
  ('60609', 'CAJAMARCA', 'CHOTA', 'LAJAS', 1),
  ('60610', 'CAJAMARCA', 'CHOTA', 'LLAMA', 1),
  ('60611', 'CAJAMARCA', 'CHOTA', 'MIRACOSTA', 1),
  ('60612', 'CAJAMARCA', 'CHOTA', 'PACCHA', 1),
  ('60613', 'CAJAMARCA', 'CHOTA', 'PION', 1),
  ('60614', 'CAJAMARCA', 'CHOTA', 'QUEROCOTO', 1),
  ('60615', 'CAJAMARCA', 'CHOTA', 'TACABAMBA', 1),
  ('60616', 'CAJAMARCA', 'CHOTA', 'TOCMOCHE', 1),
  (
    '60617',
    'CAJAMARCA',
    'CHOTA',
    'SAN JUAN DE LICUPIS',
    1
  ),
  ('60618', 'CAJAMARCA', 'CHOTA', 'CHOROPAMPA', 1),
  ('60619', 'CAJAMARCA', 'CHOTA', 'CHALAMARCA', 1),
  (
    '60701',
    'CAJAMARCA',
    'HUALGAYOC',
    'BAMBAMARCA',
    1
  ),
  ('60702', 'CAJAMARCA', 'HUALGAYOC', 'CHUGUR', 1),
  (
    '60703',
    'CAJAMARCA',
    'HUALGAYOC',
    'HUALGAYOC',
    1
  ),
  ('60801', 'CAJAMARCA', 'JAEN', 'JAEN', 1),
  ('60802', 'CAJAMARCA', 'JAEN', 'BELLAVISTA', 1),
  ('60803', 'CAJAMARCA', 'JAEN', 'COLASAY', 1),
  ('60804', 'CAJAMARCA', 'JAEN', 'CHONTALI', 1),
  ('60805', 'CAJAMARCA', 'JAEN', 'POMAHUACA', 1),
  ('60806', 'CAJAMARCA', 'JAEN', 'PUCARA', 1),
  ('60807', 'CAJAMARCA', 'JAEN', 'SALLIQUE', 1),
  ('60808', 'CAJAMARCA', 'JAEN', 'SAN FELIPE', 1),
  (
    '60809',
    'CAJAMARCA',
    'JAEN',
    'SAN JOSE DEL ALTO',
    1
  ),
  ('60810', 'CAJAMARCA', 'JAEN', 'SANTA ROSA', 1),
  ('60811', 'CAJAMARCA', 'JAEN', 'LAS PIRIAS', 1),
  ('60812', 'CAJAMARCA', 'JAEN', 'HUABAL', 1),
  (
    '60901',
    'CAJAMARCA',
    'SANTA CRUZ',
    'SANTA CRUZ',
    1
  ),
  ('60902', 'CAJAMARCA', 'SANTA CRUZ', 'CATACHE', 1),
  (
    '60903',
    'CAJAMARCA',
    'SANTA CRUZ',
    'CHANCAYBAÑOS',
    1
  ),
  (
    '60904',
    'CAJAMARCA',
    'SANTA CRUZ',
    'LA ESPERANZA',
    1
  ),
  (
    '60905',
    'CAJAMARCA',
    'SANTA CRUZ',
    'NINABAMBA',
    1
  ),
  ('60906', 'CAJAMARCA', 'SANTA CRUZ', 'PULAN', 1),
  ('60907', 'CAJAMARCA', 'SANTA CRUZ', 'SEXI', 1),
  (
    '60908',
    'CAJAMARCA',
    'SANTA CRUZ',
    'UTICYACU',
    1
  ),
  (
    '60909',
    'CAJAMARCA',
    'SANTA CRUZ',
    'YAUYUCAN',
    1
  ),
  (
    '60910',
    'CAJAMARCA',
    'SANTA CRUZ',
    'ANDABAMBA',
    1
  ),
  (
    '60911',
    'CAJAMARCA',
    'SANTA CRUZ',
    'SAUCEPAMPA',
    1
  ),
  (
    '61001',
    'CAJAMARCA',
    'SAN MIGUEL',
    'SAN MIGUEL',
    1
  ),
  ('61002', 'CAJAMARCA', 'SAN MIGUEL', 'CALQUIS', 1),
  (
    '61003',
    'CAJAMARCA',
    'SAN MIGUEL',
    'LA FLORIDA',
    1
  ),
  ('61004', 'CAJAMARCA', 'SAN MIGUEL', 'LLAPA', 1),
  ('61005', 'CAJAMARCA', 'SAN MIGUEL', 'NANCHOC', 1),
  ('61006', 'CAJAMARCA', 'SAN MIGUEL', 'NIEPOS', 1),
  (
    '61007',
    'CAJAMARCA',
    'SAN MIGUEL',
    'SAN GREGORIO',
    1
  ),
  (
    '61008',
    'CAJAMARCA',
    'SAN MIGUEL',
    'SAN SILVESTRE DE COCHAN',
    1
  ),
  (
    '61009',
    'CAJAMARCA',
    'SAN MIGUEL',
    'EL PRADO',
    1
  ),
  (
    '61010',
    'CAJAMARCA',
    'SAN MIGUEL',
    'UNION AGUA BLANCA',
    1
  ),
  ('61011', 'CAJAMARCA', 'SAN MIGUEL', 'TONGOD', 1),
  (
    '61012',
    'CAJAMARCA',
    'SAN MIGUEL',
    'CATILLUC',
    1
  ),
  ('61013', 'CAJAMARCA', 'SAN MIGUEL', 'BOLIVAR', 1),
  (
    '61101',
    'CAJAMARCA',
    'SAN IGNACIO',
    'SAN IGNACIO',
    1
  ),
  (
    '61102',
    'CAJAMARCA',
    'SAN IGNACIO',
    'CHIRINOS',
    1
  ),
  (
    '61103',
    'CAJAMARCA',
    'SAN IGNACIO',
    'HUARANGO',
    1
  ),
  (
    '61104',
    'CAJAMARCA',
    'SAN IGNACIO',
    'NAMBALLE',
    1
  ),
  (
    '61105',
    'CAJAMARCA',
    'SAN IGNACIO',
    'LA COIPA',
    1
  ),
  (
    '61106',
    'CAJAMARCA',
    'SAN IGNACIO',
    'SAN JOSE DE LOURDES',
    1
  ),
  (
    '61107',
    'CAJAMARCA',
    'SAN IGNACIO',
    'TABACONAS',
    1
  ),
  (
    '61201',
    'CAJAMARCA',
    'SAN MARCOS',
    'PEDRO GALVEZ',
    1
  ),
  ('61202', 'CAJAMARCA', 'SAN MARCOS', 'ICHOCAN', 1),
  (
    '61203',
    'CAJAMARCA',
    'SAN MARCOS',
    'GREGORIO PITA',
    1
  ),
  (
    '61204',
    'CAJAMARCA',
    'SAN MARCOS',
    'JOSE MANUEL QUIROZ',
    1
  ),
  (
    '61205',
    'CAJAMARCA',
    'SAN MARCOS',
    'EDUARDO VILLANUEVA',
    1
  ),
  (
    '61206',
    'CAJAMARCA',
    'SAN MARCOS',
    'JOSE SABOGAL',
    1
  ),
  ('61207', 'CAJAMARCA', 'SAN MARCOS', 'CHANCAY', 1),
  (
    '61301',
    'CAJAMARCA',
    'SAN PABLO',
    'SAN PABLO',
    1
  ),
  (
    '61302',
    'CAJAMARCA',
    'SAN PABLO',
    'SAN BERNARDINO',
    1
  ),
  ('61303', 'CAJAMARCA', 'SAN PABLO', 'SAN LUIS', 1),
  ('61304', 'CAJAMARCA', 'SAN PABLO', 'TUMBADEN', 1),
  ('70101', 'CUSCO', 'CUSCO', 'CUSCO', 1),
  ('70102', 'CUSCO', 'CUSCO', 'CCORCA', 1),
  ('70103', 'CUSCO', 'CUSCO', 'POROY', 1),
  ('70104', 'CUSCO', 'CUSCO', 'SAN JERONIMO', 1),
  ('70105', 'CUSCO', 'CUSCO', 'SAN SEBASTIAN', 1),
  ('70106', 'CUSCO', 'CUSCO', 'SANTIAGO', 1),
  ('70107', 'CUSCO', 'CUSCO', 'SAYLLA', 1),
  ('70108', 'CUSCO', 'CUSCO', 'WANCHAQ', 1),
  ('70201', 'CUSCO', 'ACOMAYO', 'ACOMAYO', 1),
  ('70202', 'CUSCO', 'ACOMAYO', 'ACOPIA', 1),
  ('70203', 'CUSCO', 'ACOMAYO', 'ACOS', 1),
  ('70204', 'CUSCO', 'ACOMAYO', 'POMACANCHI', 1),
  ('70205', 'CUSCO', 'ACOMAYO', 'RONDOCAN', 1),
  ('70206', 'CUSCO', 'ACOMAYO', 'SANGARARA', 1),
  ('70207', 'CUSCO', 'ACOMAYO', 'MOSOC LLACTA', 1),
  ('70301', 'CUSCO', 'ANTA', 'ANTA', 1),
  ('70302', 'CUSCO', 'ANTA', 'CHINCHAYPUJIO', 1),
  ('70303', 'CUSCO', 'ANTA', 'HUAROCONDO', 1),
  ('70304', 'CUSCO', 'ANTA', 'LIMATAMBO', 1),
  ('70305', 'CUSCO', 'ANTA', 'MOLLEPATA', 1),
  ('70306', 'CUSCO', 'ANTA', 'PUCYURA', 1),
  ('70307', 'CUSCO', 'ANTA', 'ZURITE', 1),
  ('70308', 'CUSCO', 'ANTA', 'CACHIMAYO', 1),
  ('70309', 'CUSCO', 'ANTA', 'ANCAHUASI', 1),
  ('70401', 'CUSCO', 'CALCA', 'CALCA', 1),
  ('70402', 'CUSCO', 'CALCA', 'COYA', 1),
  ('70403', 'CUSCO', 'CALCA', 'LAMAY', 1),
  ('70404', 'CUSCO', 'CALCA', 'LARES', 1),
  ('70405', 'CUSCO', 'CALCA', 'PISAC', 1),
  ('70406', 'CUSCO', 'CALCA', 'SAN SALVADOR', 1),
  ('70407', 'CUSCO', 'CALCA', 'TARAY', 1),
  ('70408', 'CUSCO', 'CALCA', 'YANATILE', 1),
  ('70501', 'CUSCO', 'CANAS', 'YANAOCA', 1),
  ('70502', 'CUSCO', 'CANAS', 'CHECCA', 1),
  ('70503', 'CUSCO', 'CANAS', 'KUNTURKANKI', 1),
  ('70504', 'CUSCO', 'CANAS', 'LANGUI', 1),
  ('70505', 'CUSCO', 'CANAS', 'LAYO', 1),
  ('70506', 'CUSCO', 'CANAS', 'PAMPAMARCA', 1),
  ('70507', 'CUSCO', 'CANAS', 'QUEHUE', 1),
  ('70508', 'CUSCO', 'CANAS', 'TUPAC AMARU', 1),
  ('70601', 'CUSCO', 'CANCHIS', 'SICUANI', 1),
  ('70602', 'CUSCO', 'CANCHIS', 'COMBAPATA', 1),
  ('70603', 'CUSCO', 'CANCHIS', 'CHECACUPE', 1),
  ('70604', 'CUSCO', 'CANCHIS', 'MARANGANI', 1),
  ('70605', 'CUSCO', 'CANCHIS', 'PITUMARCA', 1),
  ('70606', 'CUSCO', 'CANCHIS', 'SAN PABLO', 1),
  ('70607', 'CUSCO', 'CANCHIS', 'SAN PEDRO', 1),
  ('70608', 'CUSCO', 'CANCHIS', 'TINTA', 1),
  (
    '70701',
    'CUSCO',
    'CHUMBIVILCAS',
    'SANTO TOMAS',
    1
  ),
  (
    '70702',
    'CUSCO',
    'CHUMBIVILCAS',
    'CAPACMARCA',
    1
  ),
  (
    '70703',
    'CUSCO',
    'CHUMBIVILCAS',
    'COLQUEMARCA',
    1
  ),
  ('70704', 'CUSCO', 'CHUMBIVILCAS', 'CHAMACA', 1),
  ('70705', 'CUSCO', 'CHUMBIVILCAS', 'LIVITACA', 1),
  ('70706', 'CUSCO', 'CHUMBIVILCAS', 'LLUSCO', 1),
  ('70707', 'CUSCO', 'CHUMBIVILCAS', 'QUIÑOTA', 1),
  ('70708', 'CUSCO', 'CHUMBIVILCAS', 'VELILLE', 1),
  ('70801', 'CUSCO', 'ESPINAR', 'ESPINAR', 1),
  ('70802', 'CUSCO', 'ESPINAR', 'CONDOROMA', 1),
  ('70803', 'CUSCO', 'ESPINAR', 'COPORAQUE', 1),
  ('70804', 'CUSCO', 'ESPINAR', 'OCORURO', 1),
  ('70805', 'CUSCO', 'ESPINAR', 'PALLPATA', 1),
  ('70806', 'CUSCO', 'ESPINAR', 'PICHIGUA', 1),
  ('70807', 'CUSCO', 'ESPINAR', 'SUYCKUTAMBO', 1),
  ('70808', 'CUSCO', 'ESPINAR', 'ALTO PICHIGUA', 1),
  (
    '70901',
    'CUSCO',
    'LA CONVENCION',
    'SANTA ANA',
    1
  ),
  ('70902', 'CUSCO', 'LA CONVENCION', 'ECHARATE', 1),
  (
    '70903',
    'CUSCO',
    'LA CONVENCION',
    'HUAYOPATA',
    1
  ),
  ('70904', 'CUSCO', 'LA CONVENCION', 'MARANURA', 1),
  ('70905', 'CUSCO', 'LA CONVENCION', 'OCOBAMBA', 1),
  (
    '70906',
    'CUSCO',
    'LA CONVENCION',
    'SANTA TERESA',
    1
  ),
  (
    '70907',
    'CUSCO',
    'LA CONVENCION',
    'VILCABAMBA',
    1
  ),
  (
    '70908',
    'CUSCO',
    'LA CONVENCION',
    'QUELLOUNO',
    1
  ),
  ('70909', 'CUSCO', 'LA CONVENCION', 'QUIMBIRI', 1),
  ('70910', 'CUSCO', 'LA CONVENCION', 'PICHARI', 1),
  ('70911', 'CUSCO', 'LA CONVENCION', 'INKAWASI', 1),
  (
    '70912',
    'CUSCO',
    'LA CONVENCION',
    'VILLA VIRGEN',
    1
  ),
  (
    '70913',
    'CUSCO',
    'LA CONVENCION',
    'VILLA KINTIARINA',
    1
  ),
  (
    '70915',
    'CUSCO',
    'LA CONVENCION',
    'MEGANTONI',
    1
  ),
  (
    '70916',
    'CUSCO',
    'LA CONVENCION',
    'KUMPIRUSHIATO',
    1
  ),
  (
    '70917',
    'CUSCO',
    'LA CONVENCION',
    'CIELO PUNCO',
    1
  ),
  ('70918', 'CUSCO', 'LA CONVENCION', 'MANITEA', 1),
  (
    '70919',
    'CUSCO',
    'LA CONVENCION',
    'UNION ASHÁNINKA',
    1
  ),
  ('71001', 'CUSCO', 'PARURO', 'PARURO', 1),
  ('71002', 'CUSCO', 'PARURO', 'ACCHA', 1),
  ('71003', 'CUSCO', 'PARURO', 'CCAPI', 1),
  ('71004', 'CUSCO', 'PARURO', 'COLCHA', 1),
  ('71005', 'CUSCO', 'PARURO', 'HUANOQUITE', 1),
  ('71006', 'CUSCO', 'PARURO', 'OMACHA', 1),
  ('71007', 'CUSCO', 'PARURO', 'YAURISQUE', 1),
  ('71008', 'CUSCO', 'PARURO', 'PACCARITAMBO', 1),
  ('71009', 'CUSCO', 'PARURO', 'PILLPINTO', 1),
  (
    '71101',
    'CUSCO',
    'PAUCARTAMBO',
    'PAUCARTAMBO',
    1
  ),
  ('71102', 'CUSCO', 'PAUCARTAMBO', 'CAICAY', 1),
  ('71103', 'CUSCO', 'PAUCARTAMBO', 'COLQUEPATA', 1),
  (
    '71104',
    'CUSCO',
    'PAUCARTAMBO',
    'CHALLABAMBA',
    1
  ),
  ('71105', 'CUSCO', 'PAUCARTAMBO', 'KOSÑIPATA', 1),
  ('71106', 'CUSCO', 'PAUCARTAMBO', 'HUANCARANI', 1),
  ('71201', 'CUSCO', 'QUISPICANCHI', 'URCOS', 1),
  (
    '71202',
    'CUSCO',
    'QUISPICANCHI',
    'ANDAHUAYLILLAS',
    1
  ),
  ('71203', 'CUSCO', 'QUISPICANCHI', 'CAMANTI', 1),
  ('71204', 'CUSCO', 'QUISPICANCHI', 'CCARHUAYO', 1),
  ('71205', 'CUSCO', 'QUISPICANCHI', 'CCATCA', 1),
  ('71206', 'CUSCO', 'QUISPICANCHI', 'CUSIPATA', 1),
  ('71207', 'CUSCO', 'QUISPICANCHI', 'HUARO', 1),
  ('71208', 'CUSCO', 'QUISPICANCHI', 'LUCRE', 1),
  ('71209', 'CUSCO', 'QUISPICANCHI', 'MARCAPATA', 1),
  ('71210', 'CUSCO', 'QUISPICANCHI', 'OCONGATE', 1),
  ('71211', 'CUSCO', 'QUISPICANCHI', 'OROPESA', 1),
  (
    '71212',
    'CUSCO',
    'QUISPICANCHI',
    'QUIQUIJANA',
    1
  ),
  ('71301', 'CUSCO', 'URUBAMBA', 'URUBAMBA', 1),
  ('71302', 'CUSCO', 'URUBAMBA', 'CHINCHERO', 1),
  ('71303', 'CUSCO', 'URUBAMBA', 'HUAYLLABAMBA', 1),
  ('71304', 'CUSCO', 'URUBAMBA', 'MACHUPICCHU', 1),
  ('71305', 'CUSCO', 'URUBAMBA', 'MARAS', 1),
  ('71306', 'CUSCO', 'URUBAMBA', 'OLLANTAYTAMBO', 1),
  ('71307', 'CUSCO', 'URUBAMBA', 'YUCAY', 1),
  (
    '80101',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'HUANCAVELICA',
    1
  ),
  (
    '80102',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'ACOBAMBILLA',
    1
  ),
  (
    '80103',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'ACORIA',
    1
  ),
  (
    '80104',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'CONAYCA',
    1
  ),
  (
    '80105',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'CUENCA',
    1
  ),
  (
    '80106',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'HUACHOCOLPA',
    1
  ),
  (
    '80108',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'HUAYLLAHUARA',
    1
  ),
  (
    '80109',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'IZCUCHACA',
    1
  ),
  (
    '80110',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'LARIA',
    1
  ),
  (
    '80111',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'MANTA',
    1
  ),
  (
    '80112',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'MARISCAL CACERES',
    1
  ),
  (
    '80113',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'MOYA',
    1
  ),
  (
    '80114',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'NUEVO OCCORO',
    1
  ),
  (
    '80115',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'PALCA',
    1
  ),
  (
    '80116',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'PILCHACA',
    1
  ),
  (
    '80117',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'VILCA',
    1
  ),
  (
    '80118',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'YAULI',
    1
  ),
  (
    '80119',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'ASCENSION',
    1
  ),
  (
    '80120',
    'HUANCAVELICA',
    'HUANCAVELICA',
    'HUANDO',
    1
  ),
  (
    '80201',
    'HUANCAVELICA',
    'ACOBAMBA',
    'ACOBAMBA',
    1
  ),
  ('80202', 'HUANCAVELICA', 'ACOBAMBA', 'ANTA', 1),
  (
    '80203',
    'HUANCAVELICA',
    'ACOBAMBA',
    'ANDABAMBA',
    1
  ),
  ('80204', 'HUANCAVELICA', 'ACOBAMBA', 'CAJA', 1),
  ('80205', 'HUANCAVELICA', 'ACOBAMBA', 'MARCAS', 1),
  (
    '80206',
    'HUANCAVELICA',
    'ACOBAMBA',
    'PAUCARA',
    1
  ),
  (
    '80207',
    'HUANCAVELICA',
    'ACOBAMBA',
    'POMACOCHA',
    1
  ),
  (
    '80208',
    'HUANCAVELICA',
    'ACOBAMBA',
    'ROSARIO',
    1
  ),
  ('80301', 'HUANCAVELICA', 'ANGARAES', 'LIRCAY', 1),
  (
    '80302',
    'HUANCAVELICA',
    'ANGARAES',
    'ANCHONGA',
    1
  ),
  (
    '80303',
    'HUANCAVELICA',
    'ANGARAES',
    'CALLANMARCA',
    1
  ),
  (
    '80304',
    'HUANCAVELICA',
    'ANGARAES',
    'CONGALLA',
    1
  ),
  (
    '80305',
    'HUANCAVELICA',
    'ANGARAES',
    'CHINCHO',
    1
  ),
  (
    '80306',
    'HUANCAVELICA',
    'ANGARAES',
    'HUAYLLAY GRANDE',
    1
  ),
  (
    '80307',
    'HUANCAVELICA',
    'ANGARAES',
    'HUANCA-HUANCA',
    1
  ),
  (
    '80308',
    'HUANCAVELICA',
    'ANGARAES',
    'JULCAMARCA',
    1
  ),
  (
    '80309',
    'HUANCAVELICA',
    'ANGARAES',
    'SAN ANTONIO DE ANTAPARCO',
    1
  ),
  (
    '80310',
    'HUANCAVELICA',
    'ANGARAES',
    'SANTO TOMAS DE PATA',
    1
  ),
  (
    '80311',
    'HUANCAVELICA',
    'ANGARAES',
    'SECCLLA',
    1
  ),
  (
    '80312',
    'HUANCAVELICA',
    'ANGARAES',
    'CCOCHACCASA',
    1
  ),
  (
    '80401',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'CASTROVIRREYNA',
    1
  ),
  (
    '80402',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'ARMA',
    1
  ),
  (
    '80403',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'AURAHUA',
    1
  ),
  (
    '80405',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'CAPILLAS',
    1
  ),
  (
    '80406',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'COCAS',
    1
  ),
  (
    '80408',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'CHUPAMARCA',
    1
  ),
  (
    '80409',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'HUACHOS',
    1
  ),
  (
    '80410',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'HUAMATAMBO',
    1
  ),
  (
    '80414',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'MOLLEPAMPA',
    1
  ),
  (
    '80422',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'SAN JUAN',
    1
  ),
  (
    '80427',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'TANTARA',
    1
  ),
  (
    '80428',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'TICRAPO',
    1
  ),
  (
    '80429',
    'HUANCAVELICA',
    'CASTROVIRREYNA',
    'SANTA ANA',
    1
  ),
  ('80501', 'HUANCAVELICA', 'TAYACAJA', 'PAMPAS', 1),
  (
    '80502',
    'HUANCAVELICA',
    'TAYACAJA',
    'ACOSTAMBO',
    1
  ),
  (
    '80503',
    'HUANCAVELICA',
    'TAYACAJA',
    'ACRAQUIA',
    1
  ),
  (
    '80504',
    'HUANCAVELICA',
    'TAYACAJA',
    'AHUAYCHA',
    1
  ),
  (
    '80506',
    'HUANCAVELICA',
    'TAYACAJA',
    'COLCABAMBA',
    1
  ),
  (
    '80509',
    'HUANCAVELICA',
    'TAYACAJA',
    'DANIEL HERNANDEZ',
    1
  ),
  (
    '80511',
    'HUANCAVELICA',
    'TAYACAJA',
    'HUACHOCOLPA',
    1
  ),
  (
    '80512',
    'HUANCAVELICA',
    'TAYACAJA',
    'HUARIBAMBA',
    1
  ),
  (
    '80515',
    'HUANCAVELICA',
    'TAYACAJA',
    'ÑAHUIMPUQUIO',
    1
  ),
  ('80517', 'HUANCAVELICA', 'TAYACAJA', 'PAZOS', 1),
  (
    '80518',
    'HUANCAVELICA',
    'TAYACAJA',
    'QUISHUAR',
    1
  ),
  (
    '80519',
    'HUANCAVELICA',
    'TAYACAJA',
    'SALCABAMBA',
    1
  ),
  (
    '80520',
    'HUANCAVELICA',
    'TAYACAJA',
    'SAN MARCOS DE ROCCHAC',
    1
  ),
  (
    '80523',
    'HUANCAVELICA',
    'TAYACAJA',
    'SURCUBAMBA',
    1
  ),
  (
    '80525',
    'HUANCAVELICA',
    'TAYACAJA',
    'TINTAY PUNCU',
    1
  ),
  (
    '80526',
    'HUANCAVELICA',
    'TAYACAJA',
    'SALCAHUASI',
    1
  ),
  (
    '80528',
    'HUANCAVELICA',
    'TAYACAJA',
    'QUICHUAS',
    1
  ),
  (
    '80529',
    'HUANCAVELICA',
    'TAYACAJA',
    'ANDAYMARCA',
    1
  ),
  ('80530', 'HUANCAVELICA', 'TAYACAJA', 'ROBLE', 1),
  ('80531', 'HUANCAVELICA', 'TAYACAJA', 'PICHOS', 1),
  (
    '80532',
    'HUANCAVELICA',
    'TAYACAJA',
    'SANTIAGO DE TUCUMA',
    1
  ),
  (
    '80533',
    'HUANCAVELICA',
    'TAYACAJA',
    'LAMBRAS',
    1
  ),
  (
    '80534',
    'HUANCAVELICA',
    'TAYACAJA',
    'COCHABAMBA',
    1
  ),
  ('80601', 'HUANCAVELICA', 'HUAYTARA', 'AYAVI', 1),
  (
    '80602',
    'HUANCAVELICA',
    'HUAYTARA',
    'CORDOVA',
    1
  ),
  (
    '80603',
    'HUANCAVELICA',
    'HUAYTARA',
    'HUAYACUNDO ARMA',
    1
  ),
  (
    '80604',
    'HUANCAVELICA',
    'HUAYTARA',
    'HUAYTARA',
    1
  ),
  (
    '80605',
    'HUANCAVELICA',
    'HUAYTARA',
    'LARAMARCA',
    1
  ),
  ('80606', 'HUANCAVELICA', 'HUAYTARA', 'OCOYO', 1),
  (
    '80607',
    'HUANCAVELICA',
    'HUAYTARA',
    'PILPICHACA',
    1
  ),
  ('80608', 'HUANCAVELICA', 'HUAYTARA', 'QUERCO', 1),
  (
    '80609',
    'HUANCAVELICA',
    'HUAYTARA',
    'QUITO-ARMA',
    1
  ),
  (
    '80610',
    'HUANCAVELICA',
    'HUAYTARA',
    'SAN ANTONIO DE CUSICANCHA',
    1
  ),
  (
    '80611',
    'HUANCAVELICA',
    'HUAYTARA',
    'SAN FRANCISCO DE SANGAYAICO',
    1
  ),
  (
    '80612',
    'HUANCAVELICA',
    'HUAYTARA',
    'SAN ISIDRO',
    1
  ),
  (
    '80613',
    'HUANCAVELICA',
    'HUAYTARA',
    'SANTIAGO DE CHOCORVOS',
    1
  ),
  (
    '80614',
    'HUANCAVELICA',
    'HUAYTARA',
    'SANTIAGO DE QUIRAHUARA',
    1
  ),
  (
    '80615',
    'HUANCAVELICA',
    'HUAYTARA',
    'SANTO DOMINGO DE CAPILLAS',
    1
  ),
  ('80616', 'HUANCAVELICA', 'HUAYTARA', 'TAMBO', 1),
  (
    '80701',
    'HUANCAVELICA',
    'CHURCAMPA',
    'CHURCAMPA',
    1
  ),
  ('80702', 'HUANCAVELICA', 'CHURCAMPA', 'ANCO', 1),
  (
    '80703',
    'HUANCAVELICA',
    'CHURCAMPA',
    'CHINCHIHUASI',
    1
  ),
  (
    '80704',
    'HUANCAVELICA',
    'CHURCAMPA',
    'EL CARMEN',
    1
  ),
  (
    '80705',
    'HUANCAVELICA',
    'CHURCAMPA',
    'LA MERCED',
    1
  ),
  (
    '80706',
    'HUANCAVELICA',
    'CHURCAMPA',
    'LOCROJA',
    1
  ),
  (
    '80707',
    'HUANCAVELICA',
    'CHURCAMPA',
    'PAUCARBAMBA',
    1
  ),
  (
    '80708',
    'HUANCAVELICA',
    'CHURCAMPA',
    'SAN MIGUEL DE MAYOCC',
    1
  ),
  (
    '80709',
    'HUANCAVELICA',
    'CHURCAMPA',
    'SAN PEDRO DE CORIS',
    1
  ),
  (
    '80710',
    'HUANCAVELICA',
    'CHURCAMPA',
    'PACHAMARCA',
    1
  ),
  ('80711', 'HUANCAVELICA', 'CHURCAMPA', 'COSME', 1),
  ('90101', 'HUANUCO', 'HUANUCO', 'HUANUCO', 1),
  ('90102', 'HUANUCO', 'HUANUCO', 'CHINCHAO', 1),
  ('90103', 'HUANUCO', 'HUANUCO', 'CHURUBAMBA', 1),
  ('90104', 'HUANUCO', 'HUANUCO', 'MARGOS', 1),
  ('90105', 'HUANUCO', 'HUANUCO', 'QUISQUI', 1),
  (
    '90106',
    'HUANUCO',
    'HUANUCO',
    'SAN FRANCISCO DE CAYRAN',
    1
  ),
  (
    '90107',
    'HUANUCO',
    'HUANUCO',
    'SAN PEDRO DE CHAULAN',
    1
  ),
  (
    '90108',
    'HUANUCO',
    'HUANUCO',
    'SANTA MARIA DEL VALLE',
    1
  ),
  ('90109', 'HUANUCO', 'HUANUCO', 'YARUMAYO', 1),
  ('90110', 'HUANUCO', 'HUANUCO', 'AMARILIS', 1),
  ('90111', 'HUANUCO', 'HUANUCO', 'PILLCO MARCA', 1),
  ('90112', 'HUANUCO', 'HUANUCO', 'YACUS', 1),
  (
    '90113',
    'HUANUCO',
    'HUANUCO',
    'SAN PABLO DE PILLAO',
    1
  ),
  ('90201', 'HUANUCO', 'AMBO', 'AMBO', 1),
  ('90202', 'HUANUCO', 'AMBO', 'CAYNA', 1),
  ('90203', 'HUANUCO', 'AMBO', 'COLPAS', 1),
  ('90204', 'HUANUCO', 'AMBO', 'CONCHAMARCA', 1),
  ('90205', 'HUANUCO', 'AMBO', 'HUACAR', 1),
  ('90206', 'HUANUCO', 'AMBO', 'SAN FRANCISCO', 1),
  ('90207', 'HUANUCO', 'AMBO', 'SAN RAFAEL', 1),
  ('90208', 'HUANUCO', 'AMBO', 'TOMAY KICHWA', 1),
  ('90301', 'HUANUCO', 'DOS DE MAYO', 'LA UNION', 1),
  ('90307', 'HUANUCO', 'DOS DE MAYO', 'CHUQUIS', 1),
  ('90312', 'HUANUCO', 'DOS DE MAYO', 'MARIAS', 1),
  ('90314', 'HUANUCO', 'DOS DE MAYO', 'PACHAS', 1),
  ('90316', 'HUANUCO', 'DOS DE MAYO', 'QUIVILLA', 1),
  ('90317', 'HUANUCO', 'DOS DE MAYO', 'RIPAN', 1),
  ('90321', 'HUANUCO', 'DOS DE MAYO', 'SHUNQUI', 1),
  (
    '90322',
    'HUANUCO',
    'DOS DE MAYO',
    'SILLAPATA',
    1
  ),
  ('90323', 'HUANUCO', 'DOS DE MAYO', 'YANAS', 1),
  ('90401', 'HUANUCO', 'HUAMALIES', 'LLATA', 1),
  ('90402', 'HUANUCO', 'HUAMALIES', 'ARANCAY', 1),
  (
    '90403',
    'HUANUCO',
    'HUAMALIES',
    'CHAVIN DE PARIARCA',
    1
  ),
  (
    '90404',
    'HUANUCO',
    'HUAMALIES',
    'JACAS GRANDE',
    1
  ),
  ('90405', 'HUANUCO', 'HUAMALIES', 'JIRCAN', 1),
  ('90406', 'HUANUCO', 'HUAMALIES', 'MIRAFLORES', 1),
  ('90407', 'HUANUCO', 'HUAMALIES', 'MONZON', 1),
  ('90408', 'HUANUCO', 'HUAMALIES', 'PUNCHAO', 1),
  ('90409', 'HUANUCO', 'HUAMALIES', 'PUÑOS', 1),
  ('90410', 'HUANUCO', 'HUAMALIES', 'SINGA', 1),
  ('90411', 'HUANUCO', 'HUAMALIES', 'TANTAMAYO', 1),
  ('90501', 'HUANUCO', 'MARAÑON', 'HUACRACHUCO', 1),
  ('90502', 'HUANUCO', 'MARAÑON', 'CHOLON', 1),
  (
    '90505',
    'HUANUCO',
    'MARAÑON',
    'SAN BUENAVENTURA',
    1
  ),
  ('90506', 'HUANUCO', 'MARAÑON', 'LA MORADA', 1),
  (
    '90507',
    'HUANUCO',
    'MARAÑON',
    'SANTA ROSA DE ALTO YANAJANCA',
    1
  ),
  (
    '90601',
    'HUANUCO',
    'LEONCIO PRADO',
    'RUPA-RUPA',
    1
  ),
  (
    '90602',
    'HUANUCO',
    'LEONCIO PRADO',
    'DANIEL ALOMIAS ROBLES',
    1
  ),
  (
    '90603',
    'HUANUCO',
    'LEONCIO PRADO',
    'HERMILIO VALDIZAN',
    1
  ),
  (
    '90604',
    'HUANUCO',
    'LEONCIO PRADO',
    'LUYANDO',
    1
  ),
  (
    '90605',
    'HUANUCO',
    'LEONCIO PRADO',
    'MARIANO DAMASO BERAUN',
    1
  ),
  (
    '90606',
    'HUANUCO',
    'LEONCIO PRADO',
    'JOSE CRESPO Y CASTILLO',
    1
  ),
  (
    '90607',
    'HUANUCO',
    'LEONCIO PRADO',
    'PUCAYACU',
    1
  ),
  (
    '90608',
    'HUANUCO',
    'LEONCIO PRADO',
    'CASTILLO GRANDE',
    1
  ),
  (
    '90609',
    'HUANUCO',
    'LEONCIO PRADO',
    'PUEBLO NUEVO',
    1
  ),
  (
    '90610',
    'HUANUCO',
    'LEONCIO PRADO',
    'SANTO DOMINGO DE ANDA',
    1
  ),
  ('90701', 'HUANUCO', 'PACHITEA', 'PANAO', 1),
  ('90702', 'HUANUCO', 'PACHITEA', 'CHAGLLA', 1),
  ('90704', 'HUANUCO', 'PACHITEA', 'MOLINO', 1),
  ('90706', 'HUANUCO', 'PACHITEA', 'UMARI', 1),
  ('90801', 'HUANUCO', 'PUERTO INCA', 'HONORIA', 1),
  (
    '90802',
    'HUANUCO',
    'PUERTO INCA',
    'PUERTO INCA',
    1
  ),
  (
    '90803',
    'HUANUCO',
    'PUERTO INCA',
    'CODO DEL POZUZO',
    1
  ),
  (
    '90804',
    'HUANUCO',
    'PUERTO INCA',
    'TOURNAVISTA',
    1
  ),
  (
    '90805',
    'HUANUCO',
    'PUERTO INCA',
    'YUYAPICHIS',
    1
  ),
  (
    '90901',
    'HUANUCO',
    'HUACAYBAMBA',
    'HUACAYBAMBA',
    1
  ),
  ('90902', 'HUANUCO', 'HUACAYBAMBA', 'PINRA', 1),
  (
    '90903',
    'HUANUCO',
    'HUACAYBAMBA',
    'CANCHABAMBA',
    1
  ),
  (
    '90904',
    'HUANUCO',
    'HUACAYBAMBA',
    'COCHABAMBA',
    1
  ),
  ('91001', 'HUANUCO', 'LAURICOCHA', 'JESUS', 1),
  ('91002', 'HUANUCO', 'LAURICOCHA', 'BAÑOS', 1),
  (
    '91003',
    'HUANUCO',
    'LAURICOCHA',
    'SAN FRANCISCO DE ASIS',
    1
  ),
  (
    '91004',
    'HUANUCO',
    'LAURICOCHA',
    'QUEROPALCA',
    1
  ),
  (
    '91005',
    'HUANUCO',
    'LAURICOCHA',
    'SAN MIGUEL DE CAURI',
    1
  ),
  ('91006', 'HUANUCO', 'LAURICOCHA', 'RONDOS', 1),
  ('91007', 'HUANUCO', 'LAURICOCHA', 'JIVIA', 1),
  ('91101', 'HUANUCO', 'YAROWILCA', 'CHAVINILLO', 1),
  (
    '91102',
    'HUANUCO',
    'YAROWILCA',
    'APARICIO POMARES',
    1
  ),
  ('91103', 'HUANUCO', 'YAROWILCA', 'CAHUAC', 1),
  ('91104', 'HUANUCO', 'YAROWILCA', 'CHACABAMBA', 1),
  (
    '91105',
    'HUANUCO',
    'YAROWILCA',
    'JACAS CHICO',
    1
  ),
  ('91106', 'HUANUCO', 'YAROWILCA', 'OBAS', 1),
  ('91107', 'HUANUCO', 'YAROWILCA', 'PAMPAMARCA', 1),
  ('91108', 'HUANUCO', 'YAROWILCA', 'CHORAS', 1);
INSERT INTO `marca` (`id`, `nombre`)
VALUES (1, 'Volvo'),
  (2, 'Iveco'),
  (3, 'Scania'),
  (4, 'Mercedes-Benz'),
  (5, 'DAF'),
  (6, 'Renault Trucks'),
  (7, 'Hino'),
  (8, 'Mitsubishi'),
  (9, 'Isuzu'),
  (10, 'Hyundai'),
  (11, 'International'),
  (12, 'Kenworth');
INSERT INTO `tipo_unidad` (`id`, `nombre`, `descripcion`, `activo`)
VALUES (1, 'Camión', 'Vehículo de carga pesada', 1),
  (2, 'Furgoneta', 'Vehículo de carga medianaa', 0),
  (
    3,
    'Tráiler',
    'Vehículo articulado para gran volumen de carga',
    1
  ),
  (
    4,
    'Bus',
    'Vehículo de transporte de pasajeros',
    1
  ),
  (
    5,
    'Camioneta',
    'Vehículo mixto de carga y pasajeros',
    1
  );
INSERT INTO `modelo` (`id`, `nombre`, `marcaid`, `tipo_unidadid`)
VALUES (1, 'FH16', 1, 1),
  (2, 'Daily', 2, 2),
  (3, 'R-Series', 3, 1),
  (4, 'Actros', 4, 1),
  (5, 'XF', 5, 1),
  (6, 'Premium Lander', 6, 1),
  (7, '500 Series', 7, 4),
  (8, 'Fighter', 8, 1),
  (9, 'N-Series', 9, 2),
  (10, 'HD65', 10, 5),
  (11, 'ProStar', 11, 1),
  (12, 'T680', 12, 3);
INSERT INTO unidad (
    placa,
    MTC,
    TUC,
    capacidad,
    volumen,
    descripcion,
    estado,
    modeloid
  )
VALUES (
    'ABC1234',
    '1519036CNG',
    '15M25016315E',
    10.50,
    20.00,
    'Unidad para carga pesada',
    'A',
    1
  ),
  (
    'XYZ5678',
    '1519037DNG',
    '15M25016316F',
    12.00,
    25.00,
    'Camión de reparto urbano',
    'A',
    2
  ),
  (
    'JKL1234',
    '1519038ENG',
    '15M25016317G',
    15.00,
    30.00,
    'Unidad de carga mediana',
    'A',
    3
  ),
  (
    'QRS2345',
    '1519039FNG',
    '15M25016318H',
    20.00,
    35.00,
    'Camión de carga pesada',
    'A',
    4
  ),
  (
    'TUV3456',
    '1519040GNG',
    '15M25016319I',
    18.00,
    40.00,
    'Camión para transporte internacional',
    'A',
    5
  ),
  (
    'WXY4567',
    '1519041HNG',
    '15M25016320J',
    25.00,
    45.00,
    'Unidad para transporte de carga',
    'A',
    6
  ),
  (
    'LMN5678',
    '1519042ING',
    '15M25016321K',
    12.50,
    28.00,
    'Unidad para transporte pesado',
    'A',
    7
  ),
  (
    'PQR6789',
    '1519043JNG',
    '15M25016322L',
    14.00,
    30.50,
    'Camión para carga ligera',
    'A',
    8
  ),
  (
    'STU7890',
    '1519044KNG',
    '15M25016323M',
    11.00,
    23.00,
    'Unidad para transporte urbano',
    'A',
    9
  ),
  (
    'VWX8901',
    '1519045LNG',
    '15M25016324N',
    16.50,
    34.00,
    'Unidad de carga mediana',
    'A',
    10
  ),
  (
    'YZA9012',
    '1519046MNG',
    '15M25016325O',
    22.00,
    50.00,
    'Unidad para transporte pesado',
    'A',
    11
  ),
  (
    'BCD0123',
    '1519047NNG',
    '15M25016326P',
    19.00,
    40.00,
    'Camión para largo alcance',
    'A',
    12
  );
INSERT INTO tipo_indemnizacion (nombre, descripcion, activo)
VALUES (
    'Pérdida total',
    'Indemnización completa en caso de pérdida total del paquete o artículo enviado.',
    1
  ),
  (
    'Daños parciales',
    'Indemnización por daños parciales al contenido del paquete.',
    1
  ),
  (
    'Retraso en la entrega',
    'Compensación por demoras significativas en la entrega.',
    1
  ),
  (
    'Pérdida parcial',
    'Indemnización parcial en caso de pérdida parcial del contenido.',
    1
  ),
  (
    'Error en la entrega',
    'Compensación por errores en la dirección o destinatario incorrecto.',
    1
  );
INSERT INTO tipo_documento (siglas, nombre, activo)
VALUES ('DNI', 'Documento Nacional de Identidad', 1),
  ('RUC', 'Registro Único de Contribuyente', 1),
  ('CE', 'Carné de Extranjería', 1),
  ('PAS', 'Pasaporte', 1);
INSERT INTO tipo_comprobante (inicial, nombre, descripcion, activo, tipo_uso)
VALUES ('F', 'Factura', 'Factura', 1, 'V'),
  ('BV', 'Boleta', 'Boleta de Venta', 1, 'V'),
  (
    'GR',
    'Guia de remision',
    'Guía de Remisión',
    1,
    'T'
  ),
  (
    'NC',
    'Nota de crédito',
    'Nota de Crédito',
    1,
    'R'
  ),
  ('ND', 'Nota de débito', 'Nota de Débito', 1, 'R');
INSERT INTO `tipo_recepcion` (`id`, `nombre`, `activo`)
VALUES (1, 'Recepción en sucursal', 1),
  (2, 'Recepción en domicilio', 1);
INSERT INTO `tipo_empaque` (
    `id`,
    `nombre`,
    `peso_maximo`,
    `unidad_medida`,
    `activo`
  )
VALUES (1, 'Caja', 30, 'kg', 1),
  (2, 'Sobre', 5, 'gr', 1);
INSERT INTO tipo_reclamo (nombre, descripcion)
VALUES (
    'Queja',
    'Es el malestar o descontento por algún acto que está relacionado directamente con el servicio adquirido. Por ejemplo: una mala atención al público, omisión de información, etc.'
  ),
  (
    'Reclamo',
    'Es la disconformidad con los servicios prestados o bienes adquiridos. Por ejemplo: demora en el envío, entregas no realizadas, etc.'
  );
INSERT INTO motivo_reclamo (nombre, descripcion, tipo_reclamoid)
VALUES (
    'Demora en Servicio',
    'Inconformidad relacionada con la demora en la prestación del servicio.',
    2
  ),
  (
    'Temas de Facturación',
    'Inconformidad relacionada con temas de facturación, cobros incorrectos, etc.',
    2
  ),
  (
    'Extravio-Robo',
    'Inconformidad relacionada con la pérdida o robo de productos o servicios adquiridos.',
    2
  ),
  (
    'Claves de seguridad',
    'Inconformidad relacionada con el manejo, entrega o acceso a claves de seguridad.',
    2
  ),
  (
    'Atención inadecuada',
    'Es la falta de calidad en el servicio proporcionado al cliente, ya sea por parte del personal o del proceso de atención.',
    1
  );
INSERT INTO `causa_reclamo` (
    `id`,
    `nombre`,
    `descripcion`,
    `motivo_reclamoid`
  )
VALUES (
    1,
    'Daño',
    'El producto o servicio se ve afectado por un daño, lo que causa una demora en la entrega o en el servicio ofrecido.',
    1
  ),
  (
    2,
    'Mercancía Peligrosa',
    'La mercancía no puede ser procesada o transportada debido a que es peligrosa, lo que causa demoras en el servicio.',
    1
  ),
  (
    3,
    'Atasco en Máquina',
    'Un atasco o fallo en la maquinaria utilizada para el servicio o transporte causa una demora significativa.',
    1
  ),
  (
    4,
    'Envío Incompleto',
    'El envío no incluye todos los productos o elementos necesarios, lo que genera una demora adicional en la entrega final.',
    1
  ),
  (
    5,
    'Entrega Incorrecta',
    'El producto o servicio no llega al destinatario correcto, causando una demora para corregir el error.',
    1
  ),
  (
    6,
    'Incumplimiento de Lead Time',
    'El servicio no se cumple dentro del plazo acordado, generando una demora innecesaria.',
    1
  ),
  (
    7,
    'Demora Devolución de Envío y/o Cargo',
    'El proceso de devolución de productos o el manejo de cargos tiene demoras que afectan el tiempo de resolución del servicio.',
    1
  ),
  (
    8,
    'Destrucción',
    'Un evento que lleva a la destrucción del producto o servicio, causando una demora significativa en la entrega o reparación.',
    1
  ),
  (
    9,
    'Recogido No Realizado',
    'El servicio de recogida de productos no se ha realizado en el tiempo estimado, lo que causa una demora en el proceso.',
    1
  ),
  (
    10,
    'Correctamente Motivado y Dentro del Plazo',
    'El servicio está retrasado debido a una falta de motivación o coordinación dentro del plazo estipulado.',
    1
  ),
  (
    11,
    'Problemas en Registro de Envíos',
    'Los problemas relacionados con el registro del envío causan una demora en el proceso de entrega.',
    1
  ),
  (
    12,
    'No Brinda Nº de Tracking',
    'La falta de información sobre el número de seguimiento retrasa el proceso de entrega o resolución del servicio.',
    1
  ),
  (
    13,
    'Factores Externos',
    'Factores fuera del control de la empresa (como condiciones climáticas o imprevistos) que causan una demora en el servicio.',
    1
  ),
  (
    14,
    'Errores Internos',
    'Errores dentro del sistema o procesos internos que afectan la puntualidad y causan demoras.',
    1
  ),
  (
    15,
    'Sin Despachar',
    'El producto o servicio no se ha enviado, generando una demora sin justificación.',
    1
  ),
  (
    16,
    'Demora en envío de Comprobantes',
    'El comprobante de pago o factura no se envía a tiempo, causando inconvenientes con el cliente.',
    2
  ),
  (
    17,
    'Facturas/Boletas mal emitidas',
    'La facturación o boleta emitida contiene errores, lo que requiere correcciones y causa demoras en el proceso.',
    2
  ),
  (
    18,
    'Cambios: Dirección fiscal-razón social-correo',
    'Errores en la dirección fiscal, razón social o correo del cliente que deben ser corregidos para continuar con la facturación.',
    2
  ),
  (
    19,
    'Rechazo NC',
    'El rechazo de la nota de crédito causa demoras en el proceso de facturación y resolución del reclamo.',
    2
  ),
  (
    20,
    'Cliente No realizó pago',
    'El cliente no realizó el pago correspondiente, lo que afecta el proceso de facturación y entrega del servicio.',
    2
  ),
  (
    21,
    'Solicitud de dev. de dinero',
    'El cliente solicita la devolución del dinero, lo que retrasa el proceso de facturación y resolución del reclamo.',
    2
  ),
  (
    22,
    'Solicitud de envío de NC / ND',
    'El cliente solicita el envío de la nota de crédito o nota de débito, lo que causa retrasos en el proceso de facturación.',
    2
  ),
  (
    23,
    'Regularización de Pago',
    'El cliente realiza una regularización de pago, lo que genera una demora en la finalización del proceso de facturación.',
    2
  ),
  (
    24,
    'Corte de Crédito',
    'El corte de crédito impide que se continúe con el servicio hasta que el cliente resuelva su situación de pago, causando un retraso.',
    2
  ),
  (
    25,
    'Pago de Deducción',
    'El cliente realiza un pago por deducción que afecta el proceso de facturación, generando una demora en el cierre de la operación.',
    2
  ),
  (
    26,
    'Extraviado',
    'El producto o servicio ha sido extraviado durante el proceso de envío o entrega, generando la inconformidad del cliente.',
    3
  ),
  (
    27,
    'Robado',
    'El producto o servicio ha sido sustraído de manera ilícita durante el proceso de envío o entrega, lo que afecta al cliente.',
    3
  ),
  (
    28,
    'Solicita cambio de clave',
    'El cliente solicita un cambio de clave de seguridad debido a problemas con el acceso o seguridad.',
    4
  ),
  (
    29,
    'Entregado sin clave',
    'El producto o servicio fue entregado sin la clave de seguridad correspondiente, generando inconvenientes al cliente.',
    4
  ),
  (
    30,
    'No cuenta con clave',
    'El cliente no tiene acceso a la clave de seguridad requerida para completar el proceso o uso del servicio.',
    4
  ),
  (
    31,
    'Mala Atención',
    'La atención al cliente no cumple con los estándares de calidad esperados, con actitudes inadecuadas o falta de empatía.',
    5
  ),
  (
    32,
    'Demora en Atención',
    'La atención al cliente se demora más de lo esperado, generando inconvenientes y frustración para el usuario.',
    5
  ),
  (
    33,
    'Mala Conducción de Unidad',
    'El comportamiento inapropiado o deficiente por parte del personal de la unidad encargada del servicio afecta la calidad del mismo.',
    5
  );
INSERT INTO `tamanio_caja` (`id`, `nombre`, `activo`)
VALUES (1, 'XXS', 1),
  (2, 'XS', 1),
  (3, 'S', 1),
  (4, 'M', 1),
  (5, 'L', 1);
INSERT INTO contenido_paquete (nombre, activo)
VALUES ('ACCESORIOS PARA FIESTAS', 1),
  ('ACCESORIOS ELECTRÓNICOS', 1),
  ('ARTÍCULOS DE LIMPIEZA', 1),
  ('ARTÍCULOS PUBLICITARIOS', 1),
  ('BISUTERIA', 1),
  ('CAJA', 1),
  ('TARJETAS PERSONALES', 1),
  ('MUEBLES Y DECOHOGAR', 1),
  ('FERRETERÍA Y CONSTRUCCIÓN', 1),
  ('ALIMENTACION Y BEBIDAS', 1),
  ('COSMETICOS', 1),
  ('ELECTROHOGAR', 1),
  ('JUGUETES', 1),
  ('MATERIAL MEDICO', 1),
  ('MEDICINAS', 1),
  ('REPUESTOS', 1),
  ('ROPA Y ACCESORIOS', 1),
  ('VALIJA-DOCUMENTOS', 1),
  ('UTILES DE ESCRITORIO', 1),
  ('UTILES DE OFICINA', 1);
INSERT INTO articulo (
    nombre,
    precio,
    stock,
    activo,
    img,
    dimensiones,
    tamaño_cajaid
  )
VALUES (
    'Caja XXS',
    1.5,
    100,
    1,
    'caja_XXS.png',
    '10×15×10',
    1
  ),
  (
    'Caja XS',
    2,
    100,
    1,
    'caja_XS.png',
    '15×20×12',
    2
  ),
  (
    'Caja S',
    3.0,
    100,
    1,
    'caja_S.png',
    '20×30×12',
    3
  ),
  (
    'Caja M',
    3.5,
    100,
    1,
    'caja_M.png',
    '24×30×20',
    4
  ),
  (
    'Caja L',
    4,
    100,
    1,
    'caja_L.png',
    '30×42×23',
    5
  );
INSERT INTO articulo (
    nombre,
    precio,
    stock,
    activo,
    img,
    dimensiones,
    tamaño_cajaid
  )
VALUES (
    'Plumón Indeleble',
    3.00,
    100,
    1,
    'plumon.png',
    NULL,
    NULL
  ),
  (
    'Sobre A4',
    1.00,
    100,
    1,
    'sobre.png',
    '21×29.7 cm',
    NULL
  ),
  (
    'Cinta de Embalaje',
    5.90,
    100,
    1,
    'CintaEmbalaje.png',
    '48 mm × 40 m',
    NULL
  ),
  (
    'Stretch Film',
    12.00,
    100,
    1,
    'stretchfilm.png',
    'Varios tamaños',
    NULL
  ),
  (
    'Burbupack',
    2.50,
    100,
    1,
    'burbupack.png',
    '1 m × 1 m',
    NULL
  );
insert INTO `tipo_cliente` (nombre, activo)
VALUES ('Persona Natural', 1);
insert INTO `tipo_cliente` (nombre, activo)
VALUES ('Persona Jurídica', 1);
insert INTO `metodo_pago` (nombre, activo)
VALUES ('Efectivo', 1);
INSERT INTO `metodo_pago` (nombre, activo)
VALUES ('Tarjeta de Crédito', 1),
  ('Tarjeta de Débito', 1),
  ('Yape', 1);
INSERT INTO `usuario` (
    `id`,
    `correo`,
    `contrasenia`,
    `tipo_usuario`,
    `activo`
  )
VALUES (
    1,
    'ana@gmail.com',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    'E',
    1
  ),
  (
    2,
    'perez@gmail.com',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    'E',
    1
  ),
  (
    3,
    'fabs@correo.com',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    'C',
    1
  ),
  (
    4,
    'abc@gmail.com',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    'C',
    1
  ),
  (
    5,
    'abcdef@gmail.com',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    'C',
    1
  );



INSERT INTO `empleado` (`id`, `nombre`, `apellidos`, `correo`, `n_documento`, `rolid`) VALUES
(1, 'Ana', 'Ramírez', 'ana@gmail.com', '', 1),
(2, 'Juan', 'Perez', 'perez@gmail.com', '', 1),
(3, 'Carlos', 'Ramírez León', 'carlos.ramirez@transportes.com', 'D12345678', 3),
(4, 'Lucía', 'Mendoza Ruiz', 'lucia.mendoza@transportes.com', 'B98765432', 3),
(5, 'Pedro', 'Sánchez Huamán', 'pedro.sanchez@transportes.com', 'C76543210', 3),
(6, 'Ana', 'Torres Rivas', 'ana.torres@transportes.com', 'A11223344', 3),
(7, 'Luis', 'Castillo Valverde', 'luis.castillo@transportes.com', 'E55667788', 3),
(8, 'María', 'López Espinoza', 'maria.lopez@transportes.com', 'F99887766', 3),
(9, 'Javier', 'Gómez Paredes', 'javier.gomez@transportes.com', 'G33445566', 3),
(10, 'Sofía', 'Fernández Quispe', 'sofia.fernandez@transportes.com', 'H77889900', 3),
(11, 'Renzo', 'Morales Vega', 'renzo.morales@transportes.com', 'L10101010', 2),
(12, 'Karen', 'Vera Castro', 'karen.vera@transportes.com', 'L20202020', 2),
(13, 'Miguel', 'Torres Díaz', 'miguel.torres@transportes.com', 'M30303030', 4),
(14, 'Fiorella', 'Salas Gutiérrez', 'fiorella.salas@transportes.com', 'M40404040', 4),
(15, 'Valeria', 'Reyes Sánchez', 'valeria.reyes@transportes.com', 'V50505050', 5),
(16, 'Andrés', 'Cruz Ponce', 'andres.cruz@transportes.com', 'V60606060', 5),
(17, 'Lucero', 'Medina Cáceres', 'lucero.medina@transportes.com', 'D70707070', 6),
(18, 'Pablo', 'Vargas Luján', 'pablo.vargas@transportes.com', 'D80808080', 6),
(19, 'Esteban', 'Guerrero Ramírez', 'esteban.guerrero@transportes.com', 'R90909090', 7),
(20, 'Nathaly', 'Silva Aquino', 'nathaly.silva@transportes.com', 'R01010101', 7),
(21, 'Oscar', 'Huamán Ortega', 'oscar.huaman@transportes.com', 'S11111111', 8),
(22, 'Brenda', 'Campos Aguirre', 'brenda.campos@transportes.com', 'S12121212', 8),
(23, 'Ismael', 'Palacios Ruiz', 'ismael.palacios@transportes.com', 'I13131313', 9),
(24, 'Juliana', 'Ortega Paredes', 'juliana.ortega@transportes.com', 'I14141414', 9),
(25, 'Ricardo', 'Delgado Soto', 'ricardo.delgado@transportes.com', 'F15151515', 10),
(26, 'Milagros', 'León Chávez', 'milagros.leon@transportes.com', 'F16161616', 10),
(27, 'Sebastián', 'Calle Zapata', 'sebastian.calle@transportes.com', 'A17171717', 11),
(28, 'Adriana', 'García Rojas', 'adriana.garcia@transportes.com', 'A18181818', 11),
(29, 'Mario', 'Vásquez Pinto', 'mario.vasquez@transportes.com', 'V19191919', 12),
(30, 'Diana', 'Rosales Inga', 'diana.rosales@transportes.com', 'V20202020', 12),
(31, 'Alberto', 'Reyna Ríos', 'alberto.reyna@transportes.com', 'P21212121', 13),
(32, 'Valentina', 'Pérez Torres', 'valentina.perez@transportes.com', 'P22222222', 13),
(33, 'Rosa', 'Núñez Carranza', 'rosa.nunez@transportes.com', 'U23232323', 14),
(34, 'Enrique', 'Salazar Guzmán', 'enrique.salazar@transportes.com', 'U24242424', 14),
(35, 'Jimena', 'Flores Córdova', 'jimena.flores@transportes.com', 'G25252525', 15),
(36, 'Diego', 'Zamora Cornejo', 'diego.zamora@transportes.com', 'G26262626', 15);


INSERT INTO `sucursal`(
    `abreviatura`,
    `codigo_postal`,
    `direccion`,
    `horario_l_v`,
    `horario_s_d`,
    `latitud`,
    `longitud`,
    `teléfono`,
    `referencia`,
    `activo`,
    `ubigeocodigo`
  )
VALUES (
    'AMA01',
    '01001',
    'Jr. Octavio Ortiz Arrieta 270, Chachapoyas',
    '8:30am a 1pm y de 3pm a 6pm',
    '9am a 2pm',
    -6.232460,
    -77.872700,
    '',
    '',
    1,
    '10101'
  );
INSERT INTO `sucursal`(
    `abreviatura`,
    `codigo_postal`,
    `direccion`,
    `horario_l_v`,
    `horario_s_d`,
    `latitud`,
    `longitud`,
    `teléfono`,
    `referencia`,
    `activo`,
    `ubigeocodigo`
  )
VALUES (
    'AMA02',
    '',
    'Av. CAHUIDE S/N, CAMPORREDONDO, LUYA - AMAZONAS',
    '8am a 1pm y de 3pm a 6pm',
    '8am a 12pm',
    '-6.213162',
    '-78.319717',
    '',
    '',
    1,
    '10402'
  ),
  (
    'AMA03',
    '',
    'JR. MIGUEL GRAU NRO. 275, OCALLI, LUYA - AMAZONAS',
    '8am a 1pm y de 3pm a 6pm',
    '8am a 12pm',
    '-6.235146',
    '-78.266227',
    '',
    '',
    1,
    '10402'
  ),
  (
    'AMA05',
    '',
    'Jr. Mesones Muro 394, BAGUA GRANDE. Ref. Frente a la PNP',
    '8am a 6pm',
    '8am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '10701'
  ),
  (
    'AMA07',
    '',
    'JR. SAN MARTIN 199 - EL MILAGRO',
    '9am - 7:00pm',
    '9am - 7:00pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '10703'
  ),
  (
    'ANC01',
    '',
    'Av. Magdalena 240, Casma',
    '9am a 1pm y de 3pm a 7pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '20501'
  ),
  (
    'ANC02',
    '',
    'Av. Alberto Reyes 239, Huarmey',
    '9am a 1:30pm y de 4:30pm a 8:30pm',
    '9am a 2pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '21901'
  ),
  (
    'ANC03',
    '',
    'JR. INDEPENDENCIA NRO. 310, AIJA - ANCASH',
    '8am a 1pm y 4pm a 6pm',
    '8am a 1pm y 4pm a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '20201'
  ),
  (
    'ANC11',
    '',
    'Av. Ramón Castilla S/N, Cdra 8 - Caraz',
    '9am a 1pm y 3pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '20701'
  ),
  (
    'ANC12',
    '',
    'Av. Arias Graziani S/N Yungay',
    '9am a 1pm y de 3pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '21501'
  ),
  (
    'ANC13',
    '',
    'Jr. Manuel Alvarez -1065, Barrio San Bartolomé - Huari.',
    '9am a 12:30pm y de 2:30pm a 7pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '140806'
  ),
  (
    'ANC14',
    '',
    'Av. Agustín Gamarra Nro. 743, Soledad Baja - Huaraz',
    '9am a 6:30pm',
    '9am a 3pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '20101'
  ),
  (
    'ANC15',
    '',
    'Av Jose Pardo 456, Chimbote',
    'Central: 8:30am a 10pm',
    'Central: 8:30am a 9pm',
    NULL,
    NULL,
    'Frente A Plaza De Armas',
    '',
    1,
    '21301'
  ),
  (
    'ANC16',
    '',
    'AV. Pacifico Mz. S3 Lt. 36 Urb José Mariátegui, Nuevo Chimbote. Ref: Frente A La Ferretería Becor.',
    'Central: 8:30am a 8pm',
    'Central: 8:30am a 7pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '21309'
  ),
  (
    'ANC17',
    '',
    'Av. 28 De Julio 330, Sihuas',
    '8am a 1pm y de 3pm a 7pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '21410'
  ),
  (
    'APU01',
    '',
    'Jr. Elias N° 118, Abancay',
    '8am a 1pm y de 3pm a 5:30pm',
    '8am a 1pm y de 3pm a 5:30pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '30101'
  ),
  (
    'APU02',
    '',
    'Av. Panamericana Nro. 503, Curahuasi. Ref: A media cuadra del semáforo.',
    '9am a 12:30pm y de 3pm a 6pm',
    '9am a 12:30pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '30103'
  ),
  (
    'APU03',
    '',
    'Jr. Juan Francisco Ramos 559, Andahuaylas',
    '8:30am a 5pm',
    '8:30am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '30301'
  ),
  (
    'APU04',
    '',
    'Av. Panamericana # 528, Chalhuanca',
    '9am a 3pm',
    'NO HAY ATENCIÓN',
    NULL,
    NULL,
    '',
    '',
    1,
    '30201'
  ),
  (
    'APU05',
    '',
    'Av. Los Incas S/N, Uripa, Chincheros.',
    '9am a 5pm',
    '9am a 1pm',
    NULL,
    NULL,
    'Frente a la comisaría de Uripa - Anco Huallo',
    '',
    1,
    '30705'
  ),
  (
    'APU06',
    '',
    'Av. Grau 117, Chuquibambilla.',
    '9am a 1pm y de 3pm a 5pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '30601'
  ),
  (
    'ARE01',
    '',
    'Av. San José N.º 103-A, Cercado - Arequipa.',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '40102'
  ),
  (
    'ARE02',
    '',
    'Av. Parra Nro. 388, Cercado - Arequipa.',
    '9am a 6:30pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '40102'
  ),
  (
    'ARE03',
    '',
    'CALLE MAYTA CAPAC 601 IV CENTENARIO, CERCADO, AREQUIPA',
    '8:30am a 6pm',
    '9:30am a 3pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '40102'
  ),
  (
    'ARE04',
    '',
    'Av. Panamericana - Pueblo joven El Triunfo ZN B MZ A Lote 12',
    '8:30am a 1pm y de 2pm a 6pm',
    '8:30am a 2pm',
    NULL,
    NULL,
    '',
    '',
    1,
    '40106'
  );
INSERT INTO `sucursal`(
    `abreviatura`,
    `ubigeocodigo`,
    `direccion`,
    `horario_l_v`,
    `horario_s_d`,
    `latitud`,
    `longitud`,
    `teléfono`,
    `referencia`,
    `activo`,
    `codigo_postal`
  )
VALUES (
    'ARE05',
    '40105',
    'Calle Miguel Grau 214  Plaza De Las Americas, Cerro Colorado. Arequipa',
    '9am a 7pm',
    '9:30am a 3pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'ARE06',
    '40110',
    'Av. Daniel Alcides Carrión N° 269, José Luis Bustamante Rivero, Arequipa.',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM01',
    '150701',
    'Av. Primavera 275, Barranca',
    '9am a 7pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM02',
    '150107',
    'AV.- 26 DE JUNIO 405, Canta.',
    '8am a 6pm',
    'NO HAY ATENCION',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM03',
    '150502',
    'Jr. 2 De Mayo 601-D San Vicente, Cañete',
    '9am a 7pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM04',
    '150505',
    'Av. Antigua Pan. Sur 243, Mala',
    '9am a 1pm y 2pm a 6pm',
    '9am a 2pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM05',
    '150701',
    'Jr. Mariscal Castilla 117, Huacho',
    '9am a 8pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM06',
    '150603',
    'Av. Chancay Nro. 245 - Huaral. Ref. Al frente del Restaurant la Estacion.',
    '8:30am a 7pm',
    '8:30am a 6:30pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM07',
    '150602',
    'Calle Mariscal Sucre Nro. 104, Chancay. Ref: Frente a Panadería El Tanta.',
    '9am a 1pm y de 3pm a 7pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM08',
    '150603',
    'Jr. Bolognesi 398, Lurin',
    '8am a 5pm',
    '9am a 2pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'LIM09',
    '150603',
    'Plaza de armas S/N, al frente del hotel Inga, Yauyos-Lima',
    '8am a 5pm',
    'NO HAY ATENCION',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ01',
    '60101',
    'Jr. Los Nogales N° 426, Villa Universitaria, Cajamarca.',
    '9:00 am a 7:00pm',
    '9:00am a 7:00 pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ02',
    '60201',
    'Jr. Bolognesi 117, Cajabamba. Ref: Esquina del Jr. Zavala y Bologensi, a una cuadra de la RENIEC.',
    '11:00am a 1:30pm - 4:00pm a 7:30pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ03',
    '60301',
    'Esquina entre Bolognesi y Pedro Ortiz Montoya, Celendin.',
    '9am a 12pm y de 2:30pm a 6pm',
    '9am a 12pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ04',
    '60401',
    'JR. GREGORIO MALCA N° 625, Chota',
    '8:30am a 7:00 pm',
    '9:00 am a 1:00pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ05',
    '60501',
    'Jr. José Galvez S/N, Contumaza.',
    '9am a 12pm y de 3pm a 5pm',
    '9am a 12pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ06',
    '60601',
    'Jr. Contumazá 318, Chilete',
    '8am a 1pm y de 3pm a 7:30pm',
    '9am a 12pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ07',
    '60701',
    'Jr. Ramón Castilla 353, Cutervo',
    '9am a 1pm y de 3pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ08',
    '60801',
    'Jr. San Carlos 1015, Bambamarca',
    '9am a 1pm y de 3pm a 7:30pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ09',
    '60901',
    'Jr. Miguel Grau 338, San Miguel.',
    '9am a 12:30pm y de 2:30pm a 7pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ10',
    '61001',
    'Jr. Néstor Batanero Nro. 478, San Pablo.',
    '8am a 8pm',
    'NO HAY ATENCIÓN',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ11',
    '61101',
    'Entre Jr. Miguel Grau y Jr. Túpac Amaru, San Marcos.',
    '7am a 2pm / 2pm a 5pm',
    '9am a 12pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ12',
    '61201',
    'Jr. Cajamarca 484, Tembladera.',
    '8am a 7pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ13',
    '60801',
    'Calle San Martín 1255, Jaen',
    '9am a 1 pm / 3pm a 7 pm',
    '9am a 1 pm / 3pm a 7 pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ14',
    '60110',
    'Av. Lindo Nro. 150, Pucará',
    '8am a 2pm y de 4pm a 6pm',
    '8am a 2pm y de 4pm a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ15',
    '60102',
    'JR.SAN MARTIN #456 - Ref.Frente al parque principal, costado de la agencia agraria.',
    '9am a 1pm y de 3pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ16',
    '60802',
    'JR. CAUTIVO S/N, NAMBALLE, SAN IGNACIO',
    '8am a 1pm y de 3pm a 5pm',
    '8am a 1pm y de 3pm a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CAJ17',
    '60111',
    'Jr. Zarrumillas 150, Santa Cruz.',
    '8am a 12pm y de 5pm a 6pm',
    '8am a 12pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CHI01',
    '140101',
    'Mariscal Castilla 208, Chiclayo',
    '8am a 7pm',
    '9am a 7pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CHI02',
    '140102',
    'AV. Miguel Grau 675, Urb. Santa Victoria, Chiclayo',
    '9am a 1pm y de 2pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CHI03',
    '140103',
    'Av. Tacna 164, Chiclayo',
    '9am a 1pm y de 2pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CHI04',
    '140113',
    'Calle Torres Paz Nro. 224, Interior C, Pimentel',
    '9am a 1pm y de 2pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'CHI05',
    '140108',
    'Av. Huamachuco Nro. 809, Lambayeque. Frente al parque infantil.',
    '9am a 2pm y de 3pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU01',
    '120105',
    'Av. Tupac Amaru 1675 Urb Alto Mochica, Trujillo',
    '9am a 1pm y 1:45pm a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU02',
    '120105',
    'Av. Santa 1260, Trujillo Ref. A media cuadra del cruce con Av. América',
    '8am a 6pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU03',
    '120101',
    'Av. España 1234, Trujillo',
    '8am a 5pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU04',
    '120103',
    'Calle San Martín 234, Trujillo',
    '9am a 5pm',
    '9am a 1pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU05',
    '120103',
    'Jr. Los Pinos 567, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU06',
    '120109',
    'Av. América 900, Trujillo',
    '8am a 6pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU07',
    '120111',
    'Jr. Francisco Pizarro 876, Trujillo',
    '8am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU08',
    '120103',
    'Av. Larco 123, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU09',
    '120109',
    'Calle Grau 321, Trujillo',
    '8am a 6pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU10',
    '120111',
    'Av. España 789, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU11',
    '120101',
    'Jr. San Juan 456, Trujillo',
    '8am a 6pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU12',
    '120105',
    'Av. Perú 123, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU13',
    '120101',
    'Jr. Libertad 890, Trujillo',
    '8am a 6pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU14',
    '120101',
    'Av. Bolívar 456, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU15',
    '120107',
    'Calle Huamachuco 123, Trujillo',
    '8am a 6pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU16',
    '120107',
    'Av. La Marina 789, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU17',
    '120101',
    'Jr. Cajamarca 456, Trujillo',
    '8am a 6pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU18',
    '120101',
    'Av. Brasil 123, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU19',
    '120103',
    'Calle San Martín 789, Trujillo',
    '8am a 6pm',
    '9am a 5pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  ),
  (
    'TRU20',
    '120101',
    'Av. 28 de Julio 456, Trujillo',
    '9am a 7pm',
    '9am a 6pm',
    NULL,
    NULL,
    '',
    '',
    1,
    ''
  );


INSERT INTO cliente (id, correo, telefono, num_documento, nombre_siglas, apellidos_razon, tipo_documentoid, tipo_clienteid) VALUES
(1, 'fabs@correo.com', '+51 987654321', '12345678', 'Fabiola', 'Mejía', 1, 1),
(2, 'abc@gmail.com', '9726158362', '72435653', 'Ermenegildo', 'Quispe Mamani', 1, 1),
(3, 'abcdef@gmail.com', '917363282', '97264262', 'Pedro', 'Suarez Vertiz', 1, 1),
(4, 'fran@gmail.com', '83636232', '1028273672647', 'FN', 'CV', 2, 2),
(5, 'aaa@gmail.com', '76767434324', '75645375', 'Juan José', 'Paredes', 3, 2),
(6, 'ana@example.com', '987654320', '87654321', 'Ana', 'Torres', 1, 1),
(7, 'fabianapm060126@gmail.com', '987654345', '72428857', 'Liliana', 'Mejia', 1, 1),
(8, 'edgaralarconhd@gmail.com', '948811527', '71309189', 'Edgar', 'Ivan Alarcon Chapoñan', 1, 1);


INSERT INTO descuento (
    id,
    nombre,
    descripcion,
    fecha_inicio,
    fecha_fin,
    activo
  )
VALUES (
    1,
    'Descuento Volumen 25',
    'Descuento para compras a partir de 25 unidades',
    '2024-01-01',
    '2025-01-01',
    1
  ),
  (
    2,
    'Descuento Volumen 50',
    'Descuento para compras a partir de 50 unidades',
    '2024-01-01',
    '2025-01-01',
    1
  ),
  (
    3,
    'Descuento Promocional Verano',
    'Descuento especial verano 2024',
    '2024-06-01',
    '2024-08-31',
    1
  );
INSERT INTO DESCUENTO_articulo (DESCUENTOid, articuloid, cantidad_descuento)
VALUES (1, 1, 1.2),
  (1, 2, 1.7),
  (1, 3, 2.7),
  (1, 4, 3.2),
  (1, 5, 3.7),
  (2, 1, 1.0),
  (2, 2, 1.5),
  (2, 3, 2.5),
  (2, 4, 3.0),
  (2, 5, 3.5);
INSERT INTO tarifa_ruta (sucursal_origen_id, sucursal_destino_id, tarifa)
VALUES (1, 2, 12.50),
  (1, 3, 9.75),
  (1, 4, 14.20),
  (2, 3, 10.30),
  (2, 5, 19.00),
  (3, 6, 11.50),
  (4, 5, 17.00),
  (4, 7, 15.75),
  (5, 8, 13.25),
  (6, 9, 8.95),
  (7, 10, 18.00),
  (8, 11, 12.10),
  (9, 12, 16.50),
  (10, 13, 9.90),
  (11, 14, 14.40),
  (12, 15, 10.80),
  (13, 16, 19.75),
  (14, 17, 8.50),
  (15, 18, 13.95),
  (16, 19, 11.25),
  (17, 20, 18.50),
  (18, 21, 16.10),
  (19, 22, 14.75),
  (20, 23, 9.60),
  (21, 24, 12.85),
  (22, 25, 15.30),
  (23, 26, 10.15),
  (24, 27, 8.75),
  (25, 28, 17.90),
  (26, 29, 13.60),
  (27, 30, 14.95);
INSERT INTO estado_reclamo (id, nombre, activo)
VALUES (1, 'Recibido', 1),
  (2, 'Aprobado', 1),
  (3, 'Rechazado', 1),
  (4, 'En revisión', 1),
  (5, 'Resuelto', 1);
INSERT INTO detalle_reclamo (nombre, descripcion, estado_reclamoid)
VALUES (
    'Reclamo registrado',
    'El reclamo ha sido registrado exitosamente en el sistema.',
    1
  ),
  (
    'Revisión inicial',
    'El reclamo está siendo revisado por el área correspondiente.',
    4
  ),
  (
    'Solicitud aprobada',
    'El reclamo fue aprobado para su resolución.',
    2
  ),
  (
    'Solicitud rechazada',
    'El reclamo fue rechazado por no cumplir con las condiciones.',
    3
  ),
  (
    'Problema solucionado',
    'El reclamo fue resuelto y se notificó al cliente.',
    5
  ),
  (
    'Pendiente de documentos',
    'Se requiere documentación adicional del cliente.',
    4
  ),
  (
    'Validación de evidencia',
    'Se está validando la evidencia presentada.',
    4
  ),
  (
    'Reclamo confirmado',
    'El reclamo fue confirmado como procedente.',
    2
  ),
  (
    'Reclamo no procedente',
    'El reclamo fue evaluado como no procedente.',
    3
  ),
  (
    'Caso cerrado',
    'El caso fue cerrado y archivado tras resolución.',
    5
  );
INSERT INTO regla_cargo (
    id,
    tipo_condicion,
    inferior,
    superior,
    porcentaje
  )
VALUES (1, 'V', 100, 3000, 0.6);
INSERT INTO regla_cargo (
    id,
    tipo_condicion,
    inferior,
    superior,
    porcentaje
  )
VALUES (2, 'V', 3000, 10000, 2.0);
INSERT INTO regla_cargo (
    id,
    tipo_condicion,
    inferior,
    superior,
    porcentaje
  )
VALUES (3, 'P', 1, NULL, 0.1);
INSERT INTO pregunta_frecuente (titulo, descripcion, activo)
VALUES (
    '¿Qué tipos de servicios ofrecemos?',
    'Nos especializamos en ofrecer servicios de envío de carga y encomiendas a nivel nacional, con más de 250 destinos terrestres y 15 destinos aéreos. Además, facilitamos el recojo y reparto de tus envíos directamente en tu domicilio.',
    1
  ),
  (
    '¿Cuáles son los medios para realizar el pago de mi envío?',
    '<ul><li>Efectivo en cualquiera de nuestras agencias</li><li>Transferencia bancaria a nuestra cuenta corporativa</li><li>Tarjetas de débito y crédito (Visa, Mastercard)</li><li>Pago en línea a través de nuestra plataforma web</li></ul>',
    1
  ),
  (
    '¿Cómo debe realizar un correcto embalaje?',
    '<ul><li>Utilizar cajas en buen estado y del tamaño adecuado para el contenido</li><li>Proteger los artículos frágiles con material amortiguador (burbujas, papel, etc.)</li><li>Sellar todas las aberturas con cinta de embalaje resistente</li><li>Etiquetar claramente el exterior con la información de destino</li><li>No sobrecargar las cajas (máximo 25 kg por bulto)</li></ul>',
    1
  ),
  (
    '¿Cómo puedo obtener mi guía de remisión transportista?',
    '<ul><li>Solicitarla en cualquiera de nuestras agencias al momento de realizar tu envío</li><li>Descargarla directamente desde nuestra plataforma web en la sección "Mis envíos"</li><li>Recibirla por correo electrónico cuando registres tu envío</li></ul><p>Recuerda que este documento es importante para el seguimiento y control de tu envío.</p>',
    1
  );
INSERT INTO tarifa_ruta
values (28, 29, 10.00),
  (28, 30, 12.00),
  (29, 30, 10.00),
  (28, 31, 8.00),
  (28, 32, 7.00),
  (29, 31, 7.00),
  (29, 32, 8.00),
  (59, 60, 9.00),
  (60, 61, 12.00),
  (59, 61, 11.00),
  (1, 28, 9.00),
  (2, 28, 9.00),
  (28, 59, 9.00),
  (3, 5, 9.00),
  (5, 1, 7.00),
  (60, 28, 10.00);
INSERT INTO `modalidad_pago` (`id`, `nombre`, `descripcion`, `activo`)
VALUES (
    1,
    'Remitente paga en línea',
    'El remitente realiza el pago a través de medios electrónicos como tarjeta de crédito/débito, Yape u otras plataformas de pago en línea.',
    1
  ),
  (
    2,
    'Remitente paga en sucursal',
    'El remitente efectúa el pago directamente en la sucursal al momento de registrar el envío.',
    1
  ),
  (
    3,
    'Destinatario paga contraentrega',
    'El destinatario realiza el pago en el momento de recibir el paquete en su domicilio o sucursal.',
    1
  );
INSERT INTO estado_encomienda (id, nombre, descripcion, activo, tipoEstado)
VALUES (
    1,
    'En origen',
    'La encomienda aún no ha salido de la sucursal de origen.',
    1,
    'N'
  ),
  (
    2,
    'En tránsito',
    'La encomienda se encuentra viajando hacia su destino.',
    1,
    'N'
  ),
  (
    3,
    'En destino',
    'La encomienda está en la sucursal de destino o en reparto.',
    1,
    'N'
  ),
  (
    4,
    'Entregado',
    'La encomienda fue entregada satisfactoriamente al destinatario',
    1,
    'N'
  );
INSERT INTO detalle_estado (
    id,
    nombre,
    descripcion,
    activo,
    estado_encomiendaid
  )
VALUES (
    1,
    'Esperando recepción en agencia de origen',
    'Aún no se ha recibido el paquete en la sucursal de origen. Esperando que el remitente lo entregue.',
    1,
    1
  ),
  (
    2,
    'Paquete recepcionado en agencia de origen',
    'El paquete ha sido entregado por el remitente y registrado en el sistema.',
    1,
    1
  ),
  (
    3,
    'Validación de contenido y embalaje',
    'El personal de agencia verifica el embalaje y las restricciones del contenido.',
    1,
    1
  ),
  (
    4,
    'Etiqueta de tracking generada',
    'Se ha generado la etiqueta con código de seguimiento y se ha adherido al paquete.',
    1,
    1
  ),
  (
    5,
    'Clasificación interna',
    'El paquete ha sido clasificado internamente según su destino final.',
    1,
    1
  ),
  (
    6,
    'Almacenado para despacho',
    'El paquete está en la zona de salida esperando ser cargado en el vehículo de transporte.',
    1,
    1
  );
INSERT INTO detalle_estado (
    id,
    nombre,
    descripcion,
    activo,
    estado_encomiendaid
  )
VALUES (
    7,
    'Cargado en unidad de transporte',
    'El paquete ha sido cargado en la unidad de transporte interprovincial o interurbana.',
    1,
    2
  ),
  (
    8,
    'Salida de agencia de origen',
    'El vehículo con el paquete ha salido de la agencia de origen.',
    1,
    2
  ),
  (
    9,
    'En tránsito intermedio',
    'El paquete se encuentra en ruta, desplazándose hacia la ciudad de destino.',
    1,
    2
  ),
  (
    10,
    'Paso por centro logístico intermedio',
    'El paquete ha pasado por un centro de distribución o nodo intermedio.',
    1,
    2
  ),
  (
    11,
    'Revisión en control de ruta',
    'El paquete fue revisado por control en tránsito (ej. control de aduanas, pesaje, etc.).',
    1,
    2
  ),
  (
    12,
    'Próximo a llegar a destino',
    'El transporte está llegando a la agencia de destino con el paquete a bordo.',
    1,
    2
  );
INSERT INTO detalle_estado (
    id,
    nombre,
    descripcion,
    activo,
    estado_encomiendaid
  )
VALUES (
    13,
    'Recepcionado en agencia de destino',
    'El paquete ha sido descargado y registrado en la sucursal de destino.',
    1,
    3
  ),
  (
    14,
    'Clasificación para reparto',
    'El paquete ha sido clasificado y programado para reparto domiciliario.',
    1,
    3
  ),
  (
    15,
    'En espera de salida para reparto',
    'El paquete está esperando ser cargado en la unidad de reparto local.',
    1,
    3
  ),
  (
    16,
    'En ruta de entrega',
    'El paquete ha salido de la agencia y se encuentra en proceso de entrega al destinatario.',
    1,
    3
  ),
  (
    17,
    'Intento de entrega fallido',
    'Se intentó la entrega pero no hubo respuesta o no se encontró al destinatario.',
    1,
    3
  );
INSERT INTO detalle_estado (
    id,
    nombre,
    descripcion,
    activo,
    estado_encomiendaid
  )
VALUES (
    18,
    'Entregado al destinatario',
    'El paquete fue entregado correctamente al destinatario registrado.',
    1,
    4
  ),
  (
    19,
    'Recibido por tercero autorizado',
    'El paquete fue recibido por una persona autorizada diferente al destinatario.',
    1,
    4
  ),
  (
    20,
    'Firmado en conformidad',
    'El destinatario o tercero firmó como constancia de la recepción.',
    1,
    4
  ),
  (
    21,
    'Entrega validada en sistema',
    'La entrega fue confirmada en el sistema con hora y firma.',
    1,
    4
  );

INSERT INTO salida (
    fecha,
    hora,
    recojo,
    entrega,
    estado,
    unidadid,
    destino_final_id,
    conductor_principal,
    origen_inicio_id
  )
VALUES ('2025-06-16', '07:30:00', 1, 0, 'P', 1, 2, 5, 3),
  ('2025-06-16', '08:15:00', 1, 1, 'P', 2, 2, 6, 5),
  ('2025-06-16', '09:00:00', 0, 1, 'P', 3, 3, 5, 6),
  ('2025-06-16', '10:45:00', 1, 0, 'P', 4, 4, 7, 5),
  ('2025-06-16', '11:30:00', 1, 1, 'P', 5, 4, 7, 7);
INSERT INTO usuario (correo, contrasenia, tipo_usuario, activo)
VALUES (
    'carlos.ramirez@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  ),
  (
    'lucia.mendoza@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  ),
  (
    'pedro.sanchez@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  ),
  (
    'ana.torres@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  ),
  (
    'luis.castillo@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  ),
  (
    'maria.lopez@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  ),
  (
    'javier.gomez@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  ),
  (
    'sofia.fernandez@transportes.com',
    SHA2('123456', 256),
    'E',
    1
  );
INSERT INTO empleado_salida (salidaid, empleadoid)
VALUES (1, 5),
  -- Pedro Sánchez Huamán (conductor principal de salida 1)
  (1, 3),
  -- Carlos Ramírez León
  (2, 6),
  -- Ana Torres Rivas (conductor principal de salida 2)
  (2, 4),
  -- Lucía Mendoza Ruiz
  (3, 5),
  -- Pedro Sánchez Huamán (conductor principal de salida 3)
  (3, 8),
  -- María López Espinoza
  (4, 7),
  -- Luis Castillo Valverde (conductor principal de salida 4)
  (4, 9),
  -- Javier Gómez Paredes
  (5, 7),
  -- Luis Castillo Valverde (conductor principal de salida 5)
  (5, 10);
-- Sofía Fernández Quispe
INSERT INTO `detalle_estado` (
    `id`,
    `nombre`,
    `descripcion`,
    `activo`,
    `estado_encomiendaid`
  )
VALUES (
    NULL,
    'Regresado a origen',
    'No se reclamó así que se devolvió.',
    '1',
    '1'
  );


INSERT INTO `permiso` (`paginaid`, `rolid`, `acceso`, `search`, `consult`, `insert`, `update`, `delete`, `unactive`, `otro`) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(1, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(1, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(1, 15, 1, 1, 1, 1, 1, 1, 1, '{}'),
(2, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(2, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(2, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(2, 15, 1, 1, 1, 1, 1, 1, 1, '{}'),
(3, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(3, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(3, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(3, 15, 1, 1, 1, 1, 1, 1, 1, '{}'),
(4, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(4, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(4, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(4, 15, 1, 1, 1, 1, 1, 1, 0, '{}'),
(5, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(5, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(5, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(5, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(6, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(6, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(6, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(6, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(7, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(7, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(7, 13, 1, 1, 1, 1, 1, 1, 1, '{}'),
(8, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(8, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(8, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(8, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(9, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(9, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(9, 13, 1, 1, 1, 1, 1, 1, 1, '{}'),
(10, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(10, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(10, 14, 1, 1, 1, 1, 1, 1, 1, '{}'),
(11, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(11, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(11, 14, 1, 1, 1, 1, 1, 1, 1, '{}'),
(12, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(12, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(12, 14, 1, 1, 1, 1, 1, 1, 1, '{}'),
(13, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(13, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(13, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(13, 15, 0, 0, 0, 0, 0, 0, 0, '{}'),
(14, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(14, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(14, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(15, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(15, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(15, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(16, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(16, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(16, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(17, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(17, 4, 1, 1, 1, 1, 1, 1, 1, '{}'),
(17, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(17, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(17, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(18, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(18, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(18, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(18, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(19, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(19, 4, 1, 1, 1, 1, 1, 1, 1, '{}'),
(19, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(19, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(19, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(20, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(20, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(20, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(20, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(21, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(21, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(21, 13, 1, 1, 1, 1, 1, 1, 1, '{}'),
(22, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(22, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(22, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(23, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(23, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(23, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(24, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(24, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(24, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(24, 13, 1, 0, 0, 0, 0, 0, 0, '{}'),
(25, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(25, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(25, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(25, 13, 1, 0, 0, 0, 0, 0, 0, '{}'),
(25, 15, 0, 0, 0, 0, 0, 0, 0, '{}'),
(26, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(26, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(26, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(28, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(28, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(28, 14, 1, 1, 1, 1, 1, 1, 1, '{}'),
(29, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(29, 8, 0, 0, 1, 0, 0, 0, 0, '{}'),
(29, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(30, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(30, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(30, 9, 1, 1, 1, 1, 1, 1, 0, '{}'),
(31, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(31, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(31, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(32, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(32, 6, 1, 0, 0, 0, 0, 0, 0, '{}'),
(32, 7, 1, 0, 0, 0, 0, 0, 0, '{}'),
(32, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(32, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(32, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(33, 1, 1, 1, 1, 1, 1, 1, 1, '{\"mapa\": 1}'),
(33, 2, 1, 1, 1, 1, 1, 1, 1, '{}'),
(33, 4, 1, 1, 1, 1, 0, 0, 0, '{\"mapa\": 1}'),
(33, 10, 1, 1, 0, 1, 0, 0, 1, '{}'),
(33, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(33, 12, 1, 0, 0, 1, 0, 0, 0, '{\"mapa\": 1}'),
(34, 1, 1, 1, 1, 1, 1, 1, 1, '{\"paquete\": 1}'),
(34, 6, 1, 1, 1, 1, 1, 0, 0, '{\"paquete\": 1}'),
(34, 8, 1, 1, 1, 1, 1, 1, 0, '{\"paquete\": 1}'),
(34, 11, 1, 1, 1, 1, 0, 0, 0, '{\"paquete\": 1}'),
(34, 12, 1, 0, 0, 1, 0, 0, 0, '{}'),
(35, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(35, 2, 1, 1, 1, 1, 1, 1, 1, '{}'),
(35, 10, 1, 1, 0, 1, 0, 0, 1, '{}'),
(35, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(36, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(36, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(36, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(37, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(37, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(37, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(39, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(39, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(39, 13, 1, 1, 1, 1, 1, 1, 1, '{}'),
(40, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(40, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(40, 14, 1, 1, 1, 1, 1, 1, 1, '{}'),
(41, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(41, 4, 1, 0, 0, 0, 0, 0, 0, '{}'),
(41, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(41, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(41, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(42, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(42, 4, 1, 0, 0, 0, 0, 0, 0, '{}'),
(42, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(42, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(42, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(43, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(43, 4, 1, 0, 0, 0, 0, 0, 0, '{}'),
(43, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(43, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(43, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(44, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(44, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(44, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(44, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(45, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(45, 10, 1, 1, 1, 0, 0, 0, 0, '{}'),
(45, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(45, 12, 1, 1, 1, 1, 1, 1, 1, '{}'),
(46, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(46, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(46, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(47, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(47, 6, 1, 0, 0, 0, 0, 0, 0, '{}'),
(47, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(47, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(47, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(48, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(48, 2, 1, 1, 1, 1, 1, 1, 1, '{}'),
(48, 10, 1, 1, 0, 1, 0, 0, 1, '{}'),
(48, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(49, 1, 1, 1, 1, 1, 1, 1, 1, '{\"qr_code\": 1, \"seguimiento\": 1, \"encomiendas\": 1, \"pago\": 1}'),
(49, 6, 1, 1, 1, 1, 1, 0, 0, '{\"encomiendas\": 1, \"seguimiento\": 1, \"qr_code\": 1, \"pago\": 1}'),
(49, 7, 1, 1, 1, 1, 1, 1, 0, '{\"encomiendas\": 1, \"seguimiento\": 1, \"qr_code\": 1, \"pago\": 1}'),
(49, 8, 1, 1, 1, 1, 1, 1, 0, '{\"seguimiento\": 1, \"encomiendas\": 1, \"qr_code\": 1, \"pago\": 1}'),
(49, 11, 1, 1, 1, 1, 0, 0, 0, '{\"encomiendas\": 1, \"qr_code\": 1, \"seguimiento\": 1}'),
(49, 12, 1, 0, 0, 1, 0, 0, 0, '{\"encomiendas\": 1, \"qr_code\": 1}'),
(50, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(50, 8, 1, 0, 1, 0, 0, 0, 0, '{}'),
(50, 11, 1, 1, 1, 1, 1, 1, 1, '{}'),
(50, 15, 1, 0, 0, 0, 0, 0, 0, '{}'),
(51, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(51, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(51, 9, 1, 1, 1, 0, 0, 0, 0, '{}'),
(52, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(52, 2, 1, 1, 1, 1, 1, 1, 1, '{}'),
(52, 4, 1, 0, 0, 0, 0, 0, 0, '{}'),
(52, 10, 1, 1, 0, 1, 0, 0, 1, '{}'),
(52, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(52, 15, 1, 0, 0, 0, 0, 0, 0, '{}'),
(53, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(53, 6, 1, 0, 0, 0, 0, 0, 0, '{}'),
(53, 7, 1, 0, 0, 0, 0, 0, 0, '{}'),
(53, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(53, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(53, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(54, 1, 1, 1, 1, 1, 1, 1, 1, '{\"\": 1, \"paquetes\": 1}'),
(54, 6, 1, 0, 0, 1, 1, 1, 0, '{}'),
(54, 8, 1, 0, 0, 1, 1, 1, 0, '{\"paquetes\": 1}'),
(54, 11, 1, 1, 1, 1, 0, 0, 0, '{\"paquetes\": 1}'),
(54, 12, 1, 0, 0, 0, 0, 0, 0, '{}'),
(55, 1, 1, 1, 1, 1, 1, 1, 1, '{}'),
(55, 11, 1, 1, 1, 0, 0, 0, 0, '{}'),
(55, 14, 1, 1, 1, 1, 1, 1, 1, '{}'),
(56, 1, 1, 0, 0, 0, 0, 0, 0, '{}'),
(56, 6, 1, 0, 0, 0, 0, 0, 0, '{}'),
(56, 8, 1, 0, 0, 0, 0, 0, 0, '{}'),
(56, 11, 1, 1, 1, 1, 0, 0, 0, '{}'),
(57, 1, 1, 0, 0, 0, 0, 0, 0, '{}'),
(57, 5, 1, 1, 1, 1, 1, 1, 1, '{}'),
(57, 9, 1, 1, 1, 0, 0, 0, 0, '{}');


INSERT INTO transaccion_encomienda (num_serie, masivo, descripcion, monto_total, recojo_casa, id_sucursal_origen, fecha, hora, direccion_recojo, clienteid) VALUES
(22, 1, 'Envío masivo', 40.00, 0, 3, '2025-06-25', '20:27:55', NULL, 1),
(23, 1, 'Envío masivo', 23.80, 0, 16, '2025-06-25', '22:25:27', NULL, 7),
(24, 1, 'Envío masivo', 26.47, 0, 59, '2025-06-25', '22:50:12', NULL, 8),
(25, 0, 'Envío individual', 10.47, 0, 10, '2025-06-25', '22:57:32', NULL, 7);


INSERT INTO paquete (tracking, clave, valor, peso, qr_url, alto, cantidad_folios, estado_pago, largo, precio_ruta, ancho, descripcion, nombres_contacto_destinatario, apellidos_razon_destinatario, direccion_destinatario, telefono_destinatario, num_documento_destinatario, sucursal_destino_id, tipo_documento_destinatario_id, tipo_empaqueid, contenido_paqueteid, tipo_recepcionid, salidaid, transaccion_encomienda_num_serie, modalidad_pagoid) VALUES
(161, '7527', 80.00, 5.50, 'comprobantes/161/qr.png', 30.00, NULL, 'P', 45.00, 25.00, 25.00, '', 'Luis', 'Salazar', '', '987000111', '11223344', 8, 1, 1, 4, 1, NULL, 22, 1),
(162, '1245', 50.00, 1.20, 'comprobantes/162/qr.png', NULL, 10, 'P', NULL, 15.00, NULL, '', 'Lucía', 'Martínez', 'Av. Los Álamos 456, Piura', '999111222', '55667788', 10, 1, 2, NULL, 2, NULL, 22, 2),
(163, '5435', 8.00, 8.00, 'comprobantes/163/qr.png', 8.00, NULL, 'P', 8.00, 11.90, 8.00, '', 'Nayeli', 'Mestanza', 'Asturias 278', '987654345', '76543273', 19, 1, 1, 12, 2, NULL, 23, 1),
(164, '7382', 8.00, 8.00, 'comprobantes/164/qr.png', NULL, 8, 'P', NULL, 11.90, NULL, '', 'Marvil', 'Marvil', '', '907355473', '16263547', 19, 1, 2, NULL, 1, NULL, 23, 3),
(165, '1234', 200.00, 2.00, 'comprobantes/165/qr.png', 15.00, NULL, 'C', 15.00, 15.86, 15.00, '', 'Edgarcito', 'Chiquito', 'Nicolas de Pierola #163', '948811527', '71309189', 61, 1, 1, 13, 2, NULL, 24, 1),
(166, '9876', 11.00, 11.00, 'comprobantes/166/qr.png', 11.00, NULL, 'P', 11.00, 10.61, 11.00, '', 'Fabianita', 'Chiquitita', '', '923456789', '123456789', 60, 3, 1, 14, 1, NULL, 24, 2),
(167, '4356', 8.00, 8.00, 'comprobantes/167/qr.png', 8.00, NULL, 'C', 8.00, 10.47, 8.00, '', 'Ñia', 'Mejia', '', '904764673', '72527434', 13, 1, 1, 13, 1, NULL, 25, 1);





INSERT INTO transaccion_venta (num_serie, tipo_comprobanteid, estado, monto_total, fecha, hora, clienteid) VALUES
-- Ventas de Enero 2024
(1001, 1, 1, 45.50, '2024-01-15', '10:30:00', 1),
(1002, 2, 1, 128.90, '2024-01-16', '14:20:00', 3),
(1003, 1, 1, 67.30, '2024-01-18', '16:45:00', 2),
(1004, 1, 0, 34.70, '2024-01-20', '11:15:00', 4),
(1005, 1, 1, 89.20, '2024-01-25', '15:30:00', 5),

-- Ventas de Febrero 2024
(1006, 1, 1, 156.80, '2024-02-05', '09:30:00', 1),
(1007, 1, 1, 78.40, '2024-02-10', '15:20:00', 2),
(1008, 2, 1, 198.60, '2024-02-12', '13:45:00', 3),
(1009, 1, 1, 92.30, '2024-02-15', '17:30:00', 5),
(1010, 1, 1, 54.70, '2024-02-28', '12:15:00', 4),

-- Ventas de Marzo 2024
(1011, 1, 1, 234.50, '2024-03-02', '10:15:00', 4),
(1012, 1, 1, 167.80, '2024-03-08', '12:30:00', 1),
(1013, 2, 1, 345.20, '2024-03-10', '14:45:00', 3),
(1014, 1, 0, 76.40, '2024-03-15', '16:20:00', 2),
(1015, 1, 1, 123.90, '2024-03-22', '11:40:00', 5),

-- Ventas de Abril 2024
(1016, 1, 1, 189.60, '2024-04-05', '11:30:00', 5),
(1017, 1, 1, 98.70, '2024-04-12', '15:45:00', 1),
(1018, 2, 1, 278.50, '2024-04-18', '13:20:00', 3),
(1019, 1, 1, 134.20, '2024-04-25', '17:10:00', 2),
(1020, 1, 0, 45.80, '2024-04-30', '10:50:00', 4),

-- Ventas de Mayo 2024
(1021, 1, 1, 267.40, '2024-05-08', '14:25:00', 2),
(1022, 1, 1, 87.30, '2024-05-15', '16:30:00', 4),
(1023, 2, 1, 456.80, '2024-05-20', '12:15:00', 3),
(1024, 1, 1, 178.90, '2024-05-28', '18:45:00', 1),
(1025, 1, 1, 213.50, '2024-05-30', '09:20:00', 5),

-- Ventas RECIENTES (Junio 2024)
(1026, 1, 1, 324.70, '2024-06-20', '10:45:00', 2),
(1027, 1, 1, 94.60, '2024-06-21', '14:30:00', 4),
(1028, 2, 1, 567.80, '2024-06-22', '16:15:00', 3),
(1029, 1, 0, 76.20, '2024-06-23', '12:30:00', 1),
(1030, 1, 1, 145.30, '2024-06-24', '17:45:00', 5);

-- 3. DETALLES DE VENTA (productos vendidos en cada transacción)
INSERT INTO detalle_venta (articuloid, ventanum_serie, cantidad) VALUES
-- Detalles de Enero 2024
(1, 1001, 10), -- Caja XXS
(6, 1001, 5),  -- Plumón
(7, 1001, 8),  -- Sobre A4

(2, 1002, 15), -- Caja XS
(3, 1002, 20), -- Caja S
(8, 1002, 3),  -- Cinta Embalaje

(4, 1003, 8),  -- Caja M
(10, 1003, 12), -- Burbupack

(1, 1004, 5),  -- Caja XXS
(6, 1004, 2),  -- Plumón

(3, 1005, 12), -- Caja S
(5, 1005, 6),  -- Caja L

-- Detalles de Febrero 2024
(1, 1006, 25), -- Caja XXS
(2, 1006, 20), -- Caja XS
(8, 1006, 5),  -- Cinta Embalaje

(4, 1007, 10), -- Caja M
(6, 1007, 8),  -- Plumón

(5, 1008, 30), -- Caja L
(9, 1008, 4),  -- Stretch Film
(10, 1008, 15), -- Burbupack

(1, 1009, 18), -- Caja XXS
(7, 1009, 25), -- Sobre A4

(3, 1010, 8),  -- Caja S
(6, 1010, 3),  -- Plumón

-- Detalles de Marzo 2024
(2, 1011, 35), -- Caja XS
(4, 1011, 25), -- Caja M
(8, 1011, 8),  -- Cinta Embalaje

(1, 1012, 40), -- Caja XXS
(5, 1012, 15), -- Caja L

(3, 1013, 50), -- Caja S
(9, 1013, 10), -- Stretch Film
(10, 1013, 20), -- Burbupack

(1, 1014, 12), -- Caja XXS
(7, 1014, 15), -- Sobre A4

(4, 1015, 18), -- Caja M
(6, 1015, 4),  -- Plumón

-- Detalles de Abril 2024
(2, 1016, 28), -- Caja XS
(3, 1016, 22), -- Caja S
(8, 1016, 6),  -- Cinta Embalaje

(1, 1017, 20), -- Caja XXS
(10, 1017, 8), -- Burbupack

(4, 1018, 35), -- Caja M
(5, 1018, 25), -- Caja L
(9, 1018, 8),  -- Stretch Film

(2, 1019, 24), -- Caja XS
(7, 1019, 30), -- Sobre A4

(1, 1020, 8),  -- Caja XXS
(6, 1020, 2),  -- Plumón

-- Detalles de Mayo 2024
(3, 1021, 45), -- Caja S
(4, 1021, 30), -- Caja M
(8, 1021, 10), -- Cinta Embalaje

(1, 1022, 15), -- Caja XXS
(6, 1022, 5),  -- Plumón

(5, 1023, 60), -- Caja L
(9, 1023, 15), -- Stretch Film
(10, 1023, 25), -- Burbupack

(2, 1024, 38), -- Caja XS
(7, 1024, 40), -- Sobre A4

(1, 1025, 35), -- Caja XXS
(4, 1025, 28), -- Caja M

-- Detalles de Junio 2024
(3, 1026, 55), -- Caja S
(5, 1026, 40), -- Caja L
(8, 1026, 12), -- Cinta Embalaje

(1, 1027, 18), -- Caja XXS
(6, 1027, 6),  -- Plumón

(4, 1028, 65), -- Caja M
(9, 1028, 18), -- Stretch Film
(10, 1028, 30), -- Burbupack

(2, 1029, 16), -- Caja XS
(7, 1029, 20), -- Sobre A4

(1, 1030, 25), -- Caja XXS
(3, 1030, 18), -- Caja S
(6, 1030, 4);  -- Plumón

-- 4. MÉTODOS DE PAGO PARA LAS VENTAS
INSERT INTO metodo_pago_venta (num_serie, tipo_comprobante, metodo_pagoid) VALUES
-- Pagos de Enero
(1001, 1, 1), -- Efectivo
(1002, 2, 2), -- Tarjeta Crédito
(1003, 1, 3), -- Tarjeta Débito
(1004, 1, 4), -- Yape
(1005, 1, 1), -- Efectivo

-- Pagos de Febrero
(1006, 1, 2), -- Tarjeta Crédito
(1007, 1, 1), -- Efectivo
(1008, 2, 3), -- Tarjeta Débito
(1009, 1, 4), -- Yape
(1010, 1, 1), -- Efectivo

-- Pagos de Marzo
(1011, 1, 1), -- Efectivo
(1012, 1, 2), -- Tarjeta Crédito
(1013, 2, 3), -- Tarjeta Débito
(1014, 1, 4), -- Yape
(1015, 1, 1), -- Efectivo

-- Pagos de Abril
(1016, 1, 2), -- Tarjeta Crédito
(1017, 1, 1), -- Efectivo
(1018, 2, 3), -- Tarjeta Débito
(1019, 1, 4), -- Yape
(1020, 1, 1), -- Efectivo

-- Pagos de Mayo
(1021, 1, 1), -- Efectivo
(1022, 1, 2), -- Tarjeta Crédito
(1023, 2, 3), -- Tarjeta Débito
(1024, 1, 4), -- Yape
(1025, 1, 1), -- Efectivo

-- Pagos de Junio
(1026, 1, 2), -- Tarjeta Crédito
(1027, 1, 1), -- Efectivo
(1028, 2, 3), -- Tarjeta Débito
(1029, 1, 4), -- Yape
(1030, 1, 1); -- Efectivo