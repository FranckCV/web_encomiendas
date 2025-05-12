-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3307
-- Tiempo de generación: 08-05-2025 a las 14:36:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Base de datos: `bd_encomiendas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `acceso`
--

CREATE TABLE `acceso` (
  `paginaid` int(11) NOT NULL,
  `moduloid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulo`
--

CREATE TABLE `articulo` (
  `id` int(10) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(9,6) NOT NULL,
  `stock` int(11) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `tamaño_cajaid` int(11) DEFAULT NULL,
  `img` mediumblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `usuarioid` int(10) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `num_documento` varchar(20) NOT NULL,
  `nombre_siglas` varchar(150) NOT NULL,
  `apellidos_razon` varchar(150) NOT NULL,
  `tipo_documentoid` int(11) NOT NULL,
  `tipo_clienteid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `articuloid` int(10) NOT NULL,
  `cantidad` int(10) NOT NULL,
  `ventatransaccionnum_serie` int(11) NOT NULL,
  `ventatipo_comprobanteid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `usuarioid` int(10) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `apellidos` varchar(150) NOT NULL,
  `rolid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado_salida`
--

CREATE TABLE `empleado_salida` (
  `salidaid` int(10) NOT NULL,
  `empleadousuarioid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresa`
--

CREATE TABLE `empresa` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `correo` int(11) NOT NULL,
  `ruc` char(11) NOT NULL,
  `logo` mediumblob NOT NULL,
  `imagenesid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `encomienda`
--

CREATE TABLE `encomienda` (
  `tracking` int(11) NOT NULL,
  `valor` decimal(9,6) NOT NULL,
  `peso` decimal(9,6) NOT NULL,
  `alto` decimal(9,6) NOT NULL,
  `largo` decimal(9,6) NOT NULL,
  `ancho` decimal(9,6) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `direccion_destinatario` varchar(255) DEFAULT NULL,
  `num_documento_destinatario` int(11) DEFAULT NULL,
  `tipo_documento_destinatario_id` int(11) NOT NULL,
  `telefono_destinatario` int(11) DEFAULT NULL,
  `tipo_empaque` char(1) NOT NULL COMMENT 'P : Paquete\r\nS: Sobre\r\n ',
  `tipo_paqueteid` int(11) NOT NULL,
  `tipo_recojoid` int(11) NOT NULL,
  `salidaid` int(10) NOT NULL,
  `transaccion_encomienda_num_serie` int(11) DEFAULT NULL,
  `transaccion_encomienda_tipo_comprobanteid` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `escalas`
--

CREATE TABLE `escalas` (
  `sucursalid` int(10) NOT NULL,
  `salidaid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_encomienda`
--

CREATE TABLE `estado_encomienda` (
  `id` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_reclamo`
--

CREATE TABLE `estado_reclamo` (
  `id` int(10) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenes`
--

CREATE TABLE `imagenes` (
  `id` int(11) NOT NULL,
  `ruta` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

CREATE TABLE `marca` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago_venta`
--

CREATE TABLE `metodo_pago_venta` (
  `id` int(11) NOT NULL,
  `metodo_pagoid` int(11) NOT NULL,
  `num_serie` int(11) NOT NULL,
  `tipo_comprobante` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo`
--

CREATE TABLE `modelo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `marcaid` int(11) NOT NULL,
  `tipo_unidadid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modulo`
--

CREATE TABLE `modulo` (
  `id` int(11) NOT NULL,
  `Column` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagina`
--

CREATE TABLE `pagina` (
  `id` int(11) NOT NULL,
  `Column` int(11) DEFAULT NULL,
  `tipo_paginaid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reclamo`
--

CREATE TABLE `reclamo` (
  `estado_reclamoid` int(10) NOT NULL,
  `id` int(10) NOT NULL,
  `tipo_indemnizacionid` int(10) DEFAULT NULL,
  `monto_indemnizado` decimal(9,6) DEFAULT NULL,
  `paquetetracking` int(11) NOT NULL,
  `clienteid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `redes`
--

CREATE TABLE `redes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `enlace` text NOT NULL,
  `icono` text NOT NULL,
  `empresaid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(150) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `tipo_rolid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salida`
--

CREATE TABLE `salida` (
  `id` int(10) NOT NULL,
  `unidadid` int(10) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguimiento`
--

CREATE TABLE `seguimiento` (
  `estado_encomiendaid` int(10) NOT NULL,
  `paquetetracking` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursal`
--

CREATE TABLE `sucursal` (
  `id` int(10) NOT NULL,
  `direccion` varchar(150) NOT NULL,
  `ubigeocodigo` varchar(10) NOT NULL,
  `horario_l_v` varchar(255) DEFAULT NULL,
  `horario_s_d` varchar(255) DEFAULT NULL,
  `latitud` decimal(9,6) DEFAULT NULL,
  `longitud` decimal(9,6) DEFAULT NULL,
  `teléfono` char(255) DEFAULT NULL,
  `referencia` varchar(255) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tamaño_caja`
--

CREATE TABLE `tamaño_caja` (
  `id` int(11) NOT NULL,
  `nombre` varchar(3) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifa_ruta`
--

CREATE TABLE `tarifa_ruta` (
  `tarifa` decimal(9,6) NOT NULL,
  `sucursal_origen_id` int(10) NOT NULL,
  `sucursal_destino_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_cliente`
--

CREATE TABLE `tipo_cliente` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_comprobante`
--

CREATE TABLE `tipo_comprobante` (
  `id` int(10) NOT NULL,
  `nombre` char(1) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `inicial` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_documento`
--

CREATE TABLE `tipo_documento` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_indemnizacion`
--

CREATE TABLE `tipo_indemnizacion` (
  `id` int(10) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_pagina`
--

CREATE TABLE `tipo_pagina` (
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_paquete`
--

CREATE TABLE `tipo_paquete` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL COMMENT ' \r\nACCESORIOS PARA FIESTAS\r\nACCESORIOS ELECTRÓNICOS\r\nARTÍCULOS DE LIMPIEZA\r\nARTÍCULOS PUBLICITARIOS\r\nBISUTERIA\r\nCAJA\r\nTARJETAS PERSONALES\r\nMUEBLES Y DECOHOGAR\r\nFERRETERÍA Y CONSTRUCCIÓN\r\nALIMENTACION Y BEBIDAS\r\nCOSMETICOS\r\nELECTROHOGAR\r\nJUGUETES\r\nMATERIAL MEDICO\r\nMEDICINAS\r\nREPUESTOS\r\nROPA Y ACCESORIOS\r\nVALIJA-DOCUMENTOS\r\nUTILES DE ESCRITORIO\r\nUTILES DE OFICINA\r\n ',
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_recojo`
--

CREATE TABLE `tipo_recojo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL COMMENT 'Recojo en tienda\r\nEnvío a domicilio\r\nCon recojo y pago en tienda\r\n ',
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_rol`
--

CREATE TABLE `tipo_rol` (
  `id` int(10) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_unidad`
--

CREATE TABLE `tipo_unidad` (
  `id` int(10) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `descripcion` text NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transaccion_encomienda`
--

CREATE TABLE `transaccion_encomienda` (
  `num_serie` int(11) NOT NULL,
  `masivo` tinyint(1) NOT NULL COMMENT ' 1 si es envío masivo\r\n0 si es un empaque (paquete o sobre)\r\n ',
  `descripcion` varchar(255) NOT NULL,
  `monto_total` decimal(9,6) DEFAULT NULL,
  `recojo_casa` tinyint(1) NOT NULL,
  `tipo_comprobanteid` int(10) NOT NULL,
  `id_sucursal_origen` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `clienteid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `transaccion_venta`
--

CREATE TABLE `transaccion_venta` (
  `transaccionnum_serie` int(11) NOT NULL,
  `tipo_comprobanteid` int(10) NOT NULL,
  `monto_total` decimal(9,6) DEFAULT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `clienteid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ubigeo`
--

CREATE TABLE `ubigeo` (
  `codigo` varchar(10) NOT NULL,
  `departamento` varchar(150) NOT NULL,
  `provincia` varchar(150) NOT NULL,
  `distrito` varchar(150) NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unidad`
--

CREATE TABLE `unidad` (
  `id` int(10) NOT NULL,
  `placa` char(6) NOT NULL,
  `capacidad` decimal(9,2) NOT NULL,
  `volumen` decimal(9,2) NOT NULL,
  `observaciones` text DEFAULT NULL,
  `estado` char(1) NOT NULL,
  `modeloid` int(11) NOT NULL,
  `MTC` char(9) NOT NULL,
  `TUC` char(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `contrasenia` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `acceso`
--
ALTER TABLE `acceso`
  ADD PRIMARY KEY (`paginaid`,`moduloid`),
  ADD KEY `FKacceso480304` (`moduloid`);

--
-- Indices de la tabla `articulo`
--
ALTER TABLE `articulo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKarticulo75124` (`tamaño_cajaid`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`usuarioid`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `FKcliente66106` (`tipo_documentoid`),
  ADD KEY `FKcliente404372` (`tipo_clienteid`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`articuloid`,`ventatransaccionnum_serie`,`ventatipo_comprobanteid`),
  ADD KEY `FKdetalle_ve352841` (`ventatransaccionnum_serie`,`ventatipo_comprobanteid`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`usuarioid`),
  ADD KEY `FKempleado961716` (`rolid`);

--
-- Indices de la tabla `empleado_salida`
--
ALTER TABLE `empleado_salida`
  ADD PRIMARY KEY (`salidaid`,`empleadousuarioid`),
  ADD KEY `FKempleado_s308635` (`empleadousuarioid`);

--
-- Indices de la tabla `empresa`
--
ALTER TABLE `empresa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKempresa125247` (`imagenesid`);

--
-- Indices de la tabla `encomienda`
--
ALTER TABLE `encomienda`
  ADD PRIMARY KEY (`tracking`),
  ADD KEY `FKencomienda197360` (`transaccion_encomienda_num_serie`,`transaccion_encomienda_tipo_comprobanteid`),
  ADD KEY `FKencomienda483113` (`tipo_recojoid`),
  ADD KEY `FKencomienda889660` (`salidaid`),
  ADD KEY `FKencomienda794220` (`tipo_documento_destinatario_id`),
  ADD KEY `FKencomienda625453` (`tipo_paqueteid`);

--
-- Indices de la tabla `escalas`
--
ALTER TABLE `escalas`
  ADD PRIMARY KEY (`sucursalid`,`salidaid`),
  ADD KEY `FKescalas109658` (`salidaid`);

--
-- Indices de la tabla `estado_encomienda`
--
ALTER TABLE `estado_encomienda`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `estado_reclamo`
--
ALTER TABLE `estado_reclamo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `imagenes`
--
ALTER TABLE `imagenes`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `marca`
--
ALTER TABLE `marca`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `metodo_pago_venta`
--
ALTER TABLE `metodo_pago_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKmetodo_pag702897` (`metodo_pagoid`);

--
-- Indices de la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKmodelo121578` (`marcaid`),
  ADD KEY `FKmodelo83299` (`tipo_unidadid`);

--
-- Indices de la tabla `modulo`
--
ALTER TABLE `modulo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pagina`
--
ALTER TABLE `pagina`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKpagina910561` (`tipo_paginaid`);

--
-- Indices de la tabla `reclamo`
--
ALTER TABLE `reclamo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKreclamo902505` (`estado_reclamoid`),
  ADD KEY `FKreclamo501927` (`tipo_indemnizacionid`),
  ADD KEY `FKreclamo878971` (`paquetetracking`),
  ADD KEY `FKreclamo210055` (`clienteid`);

--
-- Indices de la tabla `redes`
--
ALTER TABLE `redes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKredes671243` (`empresaid`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKrol677440` (`tipo_rolid`);

--
-- Indices de la tabla `salida`
--
ALTER TABLE `salida`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKsalida314397` (`unidadid`);

--
-- Indices de la tabla `seguimiento`
--
ALTER TABLE `seguimiento`
  ADD PRIMARY KEY (`estado_encomiendaid`,`paquetetracking`),
  ADD KEY `FKseguimient816604` (`paquetetracking`);

--
-- Indices de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKsucursal756715` (`ubigeocodigo`);

--
-- Indices de la tabla `tamaño_caja`
--
ALTER TABLE `tamaño_caja`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tarifa_ruta`
--
ALTER TABLE `tarifa_ruta`
  ADD PRIMARY KEY (`sucursal_origen_id`,`sucursal_destino_id`),
  ADD KEY `FKtarifa_rut28234` (`sucursal_destino_id`);

--
-- Indices de la tabla `tipo_cliente`
--
ALTER TABLE `tipo_cliente`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_comprobante`
--
ALTER TABLE `tipo_comprobante`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_documento`
--
ALTER TABLE `tipo_documento`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_indemnizacion`
--
ALTER TABLE `tipo_indemnizacion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_pagina`
--
ALTER TABLE `tipo_pagina`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_paquete`
--
ALTER TABLE `tipo_paquete`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_recojo`
--
ALTER TABLE `tipo_recojo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_rol`
--
ALTER TABLE `tipo_rol`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_unidad`
--
ALTER TABLE `tipo_unidad`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `transaccion_encomienda`
--
ALTER TABLE `transaccion_encomienda`
  ADD PRIMARY KEY (`num_serie`,`tipo_comprobanteid`),
  ADD KEY `FKtransaccio662746` (`tipo_comprobanteid`),
  ADD KEY `FKtransaccio902557` (`clienteid`);

--
-- Indices de la tabla `transaccion_venta`
--
ALTER TABLE `transaccion_venta`
  ADD PRIMARY KEY (`transaccionnum_serie`,`tipo_comprobanteid`),
  ADD KEY `FKtransaccio293973` (`tipo_comprobanteid`),
  ADD KEY `FKtransaccio533784` (`clienteid`);

--
-- Indices de la tabla `ubigeo`
--
ALTER TABLE `ubigeo`
  ADD PRIMARY KEY (`codigo`);

--
-- Indices de la tabla `unidad`
--
ALTER TABLE `unidad`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `placa` (`placa`),
  ADD UNIQUE KEY `MTC` (`MTC`),
  ADD UNIQUE KEY `TUC` (`TUC`),
  ADD KEY `FKunidad608127` (`modeloid`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `articulo`
--
ALTER TABLE `articulo`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `usuarioid` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `usuarioid` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `empresa`
--
ALTER TABLE `empresa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `encomienda`
--
ALTER TABLE `encomienda`
  MODIFY `tracking` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estado_encomienda`
--
ALTER TABLE `estado_encomienda`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estado_reclamo`
--
ALTER TABLE `estado_reclamo`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `imagenes`
--
ALTER TABLE `imagenes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `marca`
--
ALTER TABLE `marca`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `metodo_pago_venta`
--
ALTER TABLE `metodo_pago_venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `modelo`
--
ALTER TABLE `modelo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `modulo`
--
ALTER TABLE `modulo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pagina`
--
ALTER TABLE `pagina`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reclamo`
--
ALTER TABLE `reclamo`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `redes`
--
ALTER TABLE `redes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `salida`
--
ALTER TABLE `salida`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sucursal`
--
ALTER TABLE `sucursal`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tamaño_caja`
--
ALTER TABLE `tamaño_caja`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_cliente`
--
ALTER TABLE `tipo_cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_comprobante`
--
ALTER TABLE `tipo_comprobante`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_documento`
--
ALTER TABLE `tipo_documento`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_indemnizacion`
--
ALTER TABLE `tipo_indemnizacion`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_pagina`
--
ALTER TABLE `tipo_pagina`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_paquete`
--
ALTER TABLE `tipo_paquete`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_recojo`
--
ALTER TABLE `tipo_recojo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_rol`
--
ALTER TABLE `tipo_rol`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_unidad`
--
ALTER TABLE `tipo_unidad`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `unidad`
--
ALTER TABLE `unidad`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `acceso`
--
ALTER TABLE `acceso`
  ADD CONSTRAINT `FKacceso288305` FOREIGN KEY (`paginaid`) REFERENCES `pagina` (`id`),
  ADD CONSTRAINT `FKacceso480304` FOREIGN KEY (`moduloid`) REFERENCES `modulo` (`id`);

--
-- Filtros para la tabla `articulo`
--
ALTER TABLE `articulo`
  ADD CONSTRAINT `FKarticulo75124` FOREIGN KEY (`tamaño_cajaid`) REFERENCES `tamaño_caja` (`id`);

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `FKcliente404372` FOREIGN KEY (`tipo_clienteid`) REFERENCES `tipo_cliente` (`id`),
  ADD CONSTRAINT `FKcliente66106` FOREIGN KEY (`tipo_documentoid`) REFERENCES `tipo_documento` (`id`);

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `FKdetalle_ve352841` FOREIGN KEY (`ventatransaccionnum_serie`,`ventatipo_comprobanteid`) REFERENCES `transaccion_venta` (`transaccionnum_serie`, `tipo_comprobanteid`),
  ADD CONSTRAINT `FKdetalle_ve532256` FOREIGN KEY (`articuloid`) REFERENCES `articulo` (`id`);

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `FKempleado961716` FOREIGN KEY (`rolid`) REFERENCES `rol` (`id`);

--
-- Filtros para la tabla `empleado_salida`
--
ALTER TABLE `empleado_salida`
  ADD CONSTRAINT `FKempleado_s308635` FOREIGN KEY (`empleadousuarioid`) REFERENCES `empleado` (`usuarioid`),
  ADD CONSTRAINT `FKempleado_s707218` FOREIGN KEY (`salidaid`) REFERENCES `salida` (`id`);

--
-- Filtros para la tabla `empresa`
--
ALTER TABLE `empresa`
  ADD CONSTRAINT `FKempresa125247` FOREIGN KEY (`imagenesid`) REFERENCES `imagenes` (`id`);

--
-- Filtros para la tabla `encomienda`
--
ALTER TABLE `encomienda`
  ADD CONSTRAINT `FKencomienda197360` FOREIGN KEY (`transaccion_encomienda_num_serie`,`transaccion_encomienda_tipo_comprobanteid`) REFERENCES `transaccion_encomienda` (`num_serie`, `tipo_comprobanteid`),
  ADD CONSTRAINT `FKencomienda483113` FOREIGN KEY (`tipo_recojoid`) REFERENCES `tipo_recojo` (`id`),
  ADD CONSTRAINT `FKencomienda625453` FOREIGN KEY (`tipo_paqueteid`) REFERENCES `tipo_paquete` (`id`),
  ADD CONSTRAINT `FKencomienda794220` FOREIGN KEY (`tipo_documento_destinatario_id`) REFERENCES `tipo_documento` (`id`),
  ADD CONSTRAINT `FKencomienda889660` FOREIGN KEY (`salidaid`) REFERENCES `salida` (`id`);

--
-- Filtros para la tabla `escalas`
--
ALTER TABLE `escalas`
  ADD CONSTRAINT `FKescalas109658` FOREIGN KEY (`salidaid`) REFERENCES `salida` (`id`),
  ADD CONSTRAINT `FKescalas126327` FOREIGN KEY (`sucursalid`) REFERENCES `sucursal` (`id`);

--
-- Filtros para la tabla `metodo_pago_venta`
--
ALTER TABLE `metodo_pago_venta`
  ADD CONSTRAINT `FKmetodo_pag702897` FOREIGN KEY (`metodo_pagoid`) REFERENCES `metodo_pago` (`id`);

--
-- Filtros para la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD CONSTRAINT `FKmodelo121578` FOREIGN KEY (`marcaid`) REFERENCES `marca` (`id`),
  ADD CONSTRAINT `FKmodelo83299` FOREIGN KEY (`tipo_unidadid`) REFERENCES `tipo_unidad` (`id`);

--
-- Filtros para la tabla `pagina`
--
ALTER TABLE `pagina`
  ADD CONSTRAINT `FKpagina910561` FOREIGN KEY (`tipo_paginaid`) REFERENCES `tipo_pagina` (`id`);

--
-- Filtros para la tabla `reclamo`
--
ALTER TABLE `reclamo`
  ADD CONSTRAINT `FKreclamo210055` FOREIGN KEY (`clienteid`) REFERENCES `cliente` (`usuarioid`),
  ADD CONSTRAINT `FKreclamo501927` FOREIGN KEY (`tipo_indemnizacionid`) REFERENCES `tipo_indemnizacion` (`id`),
  ADD CONSTRAINT `FKreclamo878971` FOREIGN KEY (`paquetetracking`) REFERENCES `encomienda` (`tracking`),
  ADD CONSTRAINT `FKreclamo902505` FOREIGN KEY (`estado_reclamoid`) REFERENCES `estado_reclamo` (`id`);

--
-- Filtros para la tabla `redes`
--
ALTER TABLE `redes`
  ADD CONSTRAINT `FKredes671243` FOREIGN KEY (`empresaid`) REFERENCES `empresa` (`id`);

--
-- Filtros para la tabla `rol`
--
ALTER TABLE `rol`
  ADD CONSTRAINT `FKrol677440` FOREIGN KEY (`tipo_rolid`) REFERENCES `tipo_rol` (`id`);

--
-- Filtros para la tabla `salida`
--
ALTER TABLE `salida`
  ADD CONSTRAINT `FKsalida314397` FOREIGN KEY (`unidadid`) REFERENCES `unidad` (`id`);

--
-- Filtros para la tabla `seguimiento`
--
ALTER TABLE `seguimiento`
  ADD CONSTRAINT `FKseguimient816604` FOREIGN KEY (`paquetetracking`) REFERENCES `encomienda` (`tracking`),
  ADD CONSTRAINT `FKseguimient857034` FOREIGN KEY (`estado_encomiendaid`) REFERENCES `estado_encomienda` (`id`);

--
-- Filtros para la tabla `sucursal`
--
ALTER TABLE `sucursal`
  ADD CONSTRAINT `FKsucursal756715` FOREIGN KEY (`ubigeocodigo`) REFERENCES `ubigeo` (`codigo`);

--
-- Filtros para la tabla `tarifa_ruta`
--
ALTER TABLE `tarifa_ruta`
  ADD CONSTRAINT `FKtarifa_rut28234` FOREIGN KEY (`sucursal_destino_id`) REFERENCES `sucursal` (`id`),
  ADD CONSTRAINT `FKtarifa_rut972797` FOREIGN KEY (`sucursal_origen_id`) REFERENCES `sucursal` (`id`);

--
-- Filtros para la tabla `transaccion_encomienda`
--
ALTER TABLE `transaccion_encomienda`
  ADD CONSTRAINT `FKtransaccio662746` FOREIGN KEY (`tipo_comprobanteid`) REFERENCES `tipo_comprobante` (`id`),
  ADD CONSTRAINT `FKtransaccio902557` FOREIGN KEY (`clienteid`) REFERENCES `cliente` (`usuarioid`);

--
-- Filtros para la tabla `transaccion_venta`
--
ALTER TABLE `transaccion_venta`
  ADD CONSTRAINT `FKtransaccio293973` FOREIGN KEY (`tipo_comprobanteid`) REFERENCES `tipo_comprobante` (`id`),
  ADD CONSTRAINT `FKtransaccio533784` FOREIGN KEY (`clienteid`) REFERENCES `cliente` (`usuarioid`);

--
-- Filtros para la tabla `unidad`
--
ALTER TABLE `unidad`
  ADD CONSTRAINT `FKunidad608127` FOREIGN KEY (`modeloid`) REFERENCES `modelo` (`id`);
COMMIT;
