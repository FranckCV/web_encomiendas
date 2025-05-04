-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-05-2025 a las 07:06:21
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Base de datos: `bd_encomiendas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `color`
--

CREATE TABLE `color` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `valor` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `color`
--

INSERT INTO `color` (`id`, `nombre`, `valor`) VALUES
(1, 'color1', '#370268'),
(2, 'color2', '#00c552');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

CREATE TABLE `marca` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marca`
--

INSERT INTO `marca` (`id`, `nombre`) VALUES
(1, 'Volvo'),
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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo`
--

CREATE TABLE `modelo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `marcaid` int(11) NOT NULL,
  `tipo_unidadid` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `modelo`
--



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_unidad`
--

CREATE TABLE `tipo_unidad` (
  `id` int(10) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `descripcion` text NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_unidad`
--


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ubigeo`
--

CREATE TABLE `ubigeo` (
  `codigo` char(6) NOT NULL,
  `departamento` varchar(150) NOT NULL,
  `distrito` varchar(150) NOT NULL,
  `provincia` varchar(150) NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ubigeo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unidad`
--

CREATE TABLE `unidad` (
  `id` int(10) NOT NULL,
  `placa` varchar(10) NOT NULL,
  `capacidad` decimal(9,2) NOT NULL,
  `volumen` decimal(9,2) NOT NULL,
  `observaciones` text DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `modeloid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `unidad`
--

-- INSERT INTO `unidad` (`id`, `placa`, `capacidad`, `volumen`, `observaciones`, `activo`, `modeloid`) VALUES
-- (1, 'ABC123f', 15000.00, 60.00, 'Unidad en buen estado', 1, 1),
-- (2, 'DEF456', 4000.00, 20.00, 'Requiere revisión técnica', 0, 2),
-- (3, 'GHI789', 30000.00, 80.00, NULL, 1, 12),
-- (4, 'JKL321', 8000.00, 50.00, 'Unidad fuera de servicio', 0, 7),
-- (5, 'MNO654', 2500.00, 10.00, 'Unidad nueva', 1, 10),
-- (6, 'PQR987', 1500.00, 60.00, 'None', 1, 3),
-- (7, 'STU135', 4000.00, 20.00, 'Unidad asignada a ruta norte', 1, 9),
-- (8, 'VWX246', 8000.00, 50.00, 'Con aire acondicionado', 1, 4);

-- --
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `color`
--
ALTER TABLE `color`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `marca`
--
ALTER TABLE `marca`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKmodelo121578` (`marcaid`),
  ADD KEY `FKmodelo83299` (`tipo_unidadid`);

--
-- Indices de la tabla `tipo_unidad`
--
ALTER TABLE `tipo_unidad`
  ADD PRIMARY KEY (`id`);

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
  ADD KEY `FKunidad608127` (`modeloid`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `color`
--
ALTER TABLE `color`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `marca`
--
ALTER TABLE `marca`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `modelo`
--
ALTER TABLE `modelo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `tipo_unidad`
--
ALTER TABLE `tipo_unidad`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `unidad`
--
ALTER TABLE `unidad`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD CONSTRAINT `FKmodelo121578` FOREIGN KEY (`marcaid`) REFERENCES `marca` (`id`),
  ADD CONSTRAINT `FKmodelo83299` FOREIGN KEY (`tipo_unidadid`) REFERENCES `tipo_unidad` (`id`);

--
-- Filtros para la tabla `unidad`
--
ALTER TABLE `unidad`
  ADD CONSTRAINT `FKunidad608127` FOREIGN KEY (`modeloid`) REFERENCES `modelo` (`id`);
COMMIT;
---TABLA TIPO_RECOJO
CREATE TABLE tipo_recojo (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  PRIMARY KEY (id));

--   INSERT INTO tipo_recojo (nombre) VALUES ('Recojo en tienda');
-- INSERT INTO tipo_recojo (nombre) VALUES ('Envío a domicilio');
-- INSERT INTO tipo_recojo (nombre) VALUES ('Con recojo y pago en tienda');
