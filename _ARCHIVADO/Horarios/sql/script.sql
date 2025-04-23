-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 31-12-2024 a las 15:36:26
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Base de datos: bd_horario
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla alumno
--

CREATE TABLE alumno (
  id int(11) NOT NULL,
  nombres varchar(150) NOT NULL,
  apellidos varchar(150) NOT NULL,
  codigo varchar(20) NOT NULL,
  contrasenia varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla alumno
--

INSERT INTO alumno (id, nombres, apellidos, codigo, contrasenia) VALUES
(1, 'yo', 'xd', '221VP21182', '123'),
(2, 'test', 'cha', 'abc', 'abc'),
(3, 'test', 'cachimbo', 'abcd', 'abc');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla color
--

CREATE TABLE color (
  id int(11) NOT NULL,
  nombre varchar(15) NOT NULL,
  color_fondo varchar(15) NOT NULL,
  color_texto varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla color
--

INSERT INTO color (id, nombre, color_fondo, color_texto) VALUES
(1, 'rojo', 'darkred', 'white'),
(2, 'azul', 'darkblue', 'white'),
(3, 'verde', 'green', 'white'),
(4, 'amarillo', 'yellow', 'black'),
(5, 'naranja', 'orange', 'white'),
(6, 'morado', 'purple', 'white'),
(7, '7mo', '#333F4F', 'white'),
(8, 'pa taller', 'darkgrey', 'white');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla curso
--

CREATE TABLE curso (
  id int(11) NOT NULL,
  abreviacion varchar(6) NOT NULL,
  nombre varchar(255) NOT NULL,
  creditos int(11) NOT NULL,
  ciclo int(11) NOT NULL,
  colorid int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla curso
--

INSERT INTO curso (id, abreviacion, nombre, creditos, ciclo, colorid) VALUES
(1, 'DAW', 'Desarrollo de Aplicaciones Web', 4, 6, 3),
(2, 'DAE', 'Desarrollo de Aplicaciones de Escritorio', 4, 6, 2),
(3, 'IA', 'Inteligencia Artificial', 4, 6, 5),
(4, 'FC', 'Fe y Cultura', 3, 6, 6),
(5, 'INVOPE', 'Investigación en Operaciones', 3, 6, 4),
(6, 'SO', 'Sistemas Operativos', 3, 6, 1),
(7, 'DW', 'Diseño Web', 3, 5, 3),
(8, 'BD', 'Base de Datos', 4, 4, 4),
(9, 'ANTRO', 'Antropologia Filosofica', 3, 4, 6),
(10, 'ED', 'Ecuaciones Diferenciales y Métodos Númericos', 4, 4, 5),
(11, 'CRB', 'Comprensión De Textos Y Redacción Básica', 3, 1, 6),
(12, 'DCD', 'Desarrollo De Competencias Digitales', 2, 1, 3),
(13, 'EST', 'Estrategias Para El Aprendizaje Autónomo', 3, 1, 7),
(14, 'IISC', 'Introducción A La Ingeniería De Sistemas Y Computación', 3, 1, 4),
(15, 'MB', 'Matemática Básica', 3, 1, 5),
(16, 'MD', 'Matemática Discreta', 4, 1, 2),
(17, 'CUV', 'Cálculo De Una Variable', 4, 2, 5),
(18, 'CRTA', 'Comprensión Y Redacción De Textos Académicos', 3, 2, 6),
(19, 'ECOL', 'Ecología Y Desarrollo Sostenible', 3, 2, 7),
(20, 'ECON', 'Economía Y Realidad Nacional', 3, 2, 4),
(21, 'FPR', 'Fundamentos De Programación', 3, 2, 2),
(22, 'TPO', 'Teoría Y Procesos Organizacionales', 3, 2, 3),
(23, 'AER', 'Análisis Y Especificación De Requisitos', 3, 3, 3),
(24, 'CVV', 'Cálculo De Varias Variables', 4, 3, 5),
(25, 'CONTA', 'Contabilidad Y Finanzas', 3, 3, 4),
(26, 'FILO', 'Filosofía', 3, 3, 6),
(27, 'FIS', 'Física De Los Cuerpos Rígidos', 4, 3, 1),
(28, 'MPR', 'Metodologías De Programación', 3, 3, 2),
(29, 'DS', 'Diseño De Software', 3, 4, 3),
(30, 'EM', 'Electricidad Y Magnetismo', 4, 4, 1),
(31, 'EDA', 'Estructura De Datos Y Algoritmos', 3, 4, 2),
(32, 'ABD', 'Administración De Base De Datos', 3, 5, 2),
(33, 'AOC', 'Arquitectura Y Organización De Computadoras', 4, 5, 1),
(34, 'EP', 'Estadística Y Probabilidades', 3, 5, 5),
(35, 'ETI', 'Ética', 3, 5, 6),
(36, 'IP', 'Ingeniería De Procesos', 3, 5, 4),
(37, 'TGS', 'Teoría General De Sistemas', 2, 5, 7),
(38, 'BSKT', 'Taller de Basket', 1, 0, 8),
(39, 'DSI', 'Desarrollo De Sistemas Inteligentes', 2, 7, 5),
(40, 'FDRD', 'Fundamentos Y Diseño De Redes De Datos', 3, 7, 1),
(41, 'ICS', 'Ingeniería Y Calidad De Software', 4, 7, 2),
(42, 'IN', 'Inteligencia De Negocios', 3, 7, 7),
(43, 'IEI', 'Investigación En Ingeniería', 3, 7, 4),
(44, 'MC', 'Moral Católica', 3, 7, 6),
(45, 'SD', 'Sistemas Distribuidos', 3, 7, 3),
(46, 'CARD', 'Configuración Y Administración De Redes De Datos', 4, 8, 1),
(47, 'DAM', 'Desarrollo De Aplicaciones Móviles', 4, 8, 3),
(48, 'DSI', 'Doctrina Social De La Iglesia', 3, 8, 6),
(49, 'GGTI', 'Gobierno Y Gestión De Tecnologías De Información', 4, 8, 2),
(50, 'MDBD', 'Minería De Datos Y Big Data', 3, 8, 5),
(51, 'PI', 'Proyecto De Investigación', 3, 8, 4),
(52, 'X', 'Configuración Y Administración De Servidores', 4, 9, 1),
(53, 'X', 'Deontología Y Legislación Laboral E Informática', 2, 9, 6),
(54, 'X', 'Gestión De Riesgos Y Seguridad De La Información', 4, 9, 7),
(55, 'X', 'Gestión De Servicios De Tecnologías De Información', 4, 9, 2),
(56, 'X', 'Negocios Electrónicos Y Marketing Digital', 4, 9, 5),
(57, 'X', 'Seminario De Tesis I', 3, 9, 4),
(58, 'X', 'Auditoría De Sistemas De Información', 4, 10, 7),
(59, 'X', 'Desarrollo De Video Juegos', 2, 10, 7),
(60, 'X', 'Emprendimiento De Base Tecnológica', 2, 10, 5),
(61, 'X', 'Gestión De Proyectos De Sistemas De Información', 4, 10, 2),
(62, 'X', 'Seguridad Informática', 3, 10, 1),
(63, 'X', 'Seminario De Tesis II', 3, 10, 4),
(64, 'X', 'Sistemas ERP', 2, 10, 7),
(65, 'X', 'Tópicos Avanzados En Desarrollo De Software', 3, 10, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla curso_curso
--

CREATE TABLE curso_curso (
  cursoid int(11) NOT NULL,
  cursoid_pre int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla curso_curso
--

INSERT INTO curso_curso (cursoid, cursoid_pre) VALUES
(1, 7),
(1, 32),
(2, 32),
(3, 34),
(4, 35),
(5, 34),
(6, 33),
(7, 29),
(8, 23),
(8, 25),
(9, 26),
(10, 24),
(17, 15),
(18, 11),
(19, 13),
(20, 14),
(21, 15),
(21, 16),
(22, 12),
(23, 22),
(24, 17),
(25, 20),
(26, 18),
(27, 17),
(28, 21),
(29, 23),
(30, 27),
(31, 28),
(32, 8),
(32, 31),
(33, 30),
(34, 10),
(35, 9),
(36, 29),
(37, 9),
(39, 3),
(40, 6),
(41, 2),
(42, 32),
(43, 5),
(44, 4),
(45, 1),
(46, 40),
(47, 45),
(48, 44),
(49, 41),
(50, 39),
(50, 42),
(51, 43),
(52, 46),
(53, 48),
(54, 49),
(55, 49),
(56, 50),
(57, 47),
(57, 51),
(58, 54),
(59, 47),
(60, 56),
(61, 55),
(62, 52),
(63, 57),
(64, 47),
(65, 57);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla detalles_matricula
--

CREATE TABLE detalles_matricula (
  grupoid int(11) NOT NULL,
  matriculaid int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla detalles_matricula
--

INSERT INTO detalles_matricula (grupoid, matriculaid) VALUES
(1, 6),
(2, 6),
(3, 6),
(3, 12),
(4, 6),
(4, 12),
(5, 6),
(6, 6),
(7, 4),
(7, 10),
(7, 11),
(7, 12),
(8, 4),
(8, 10),
(9, 4),
(9, 11),
(10, 4),
(10, 10),
(11, 1),
(11, 7),
(12, 1),
(12, 7),
(13, 1),
(13, 7),
(14, 3),
(14, 9),
(15, 4),
(15, 11),
(16, 2),
(16, 8),
(17, 3),
(17, 9),
(17, 10),
(18, 4),
(18, 10),
(19, 3),
(19, 9),
(20, 3),
(20, 9),
(20, 10),
(21, 2),
(21, 8),
(22, 5),
(22, 11),
(23, 1),
(23, 7),
(24, 1),
(24, 7),
(25, 5),
(25, 11),
(26, 5),
(27, 5),
(27, 11),
(28, 5),
(28, 12),
(29, 5),
(29, 12),
(30, 5),
(31, 1),
(31, 7),
(32, 2),
(32, 8),
(33, 2),
(33, 8),
(34, 2),
(34, 8),
(35, 2),
(35, 8),
(36, 3),
(36, 9),
(37, 3),
(37, 9),
(38, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla docente
--

CREATE TABLE docente (
  id int(11) NOT NULL,
  nombres varchar(150) NOT NULL,
  apellidos varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla docente
--

INSERT INTO docente (id, nombres, apellidos) VALUES
(1, 'Junior Eugenio', 'Cachay Maco'),
(2, 'Roger Ernesto', 'Alarcon Garcia'),
(3, 'Karla Cecilia', 'Reyes Burgos'),
(4, 'Alicia Lizet', 'Niño Effio'),
(5, 'Absalon', 'Rivasplata Sanchez'),
(6, 'Edwar Glorimer', 'Lujan Segura'),
(7, 'Julio Cesar', 'Moreno Descalzi'),
(8, 'Luis Augusto', 'Zuñe Bispo'),
(9, 'Alexander Omar', 'Cruzado Quiroz'),
(10, 'Gregorio Manuel', 'Leon Tenorio'),
(11, 'Marco Antonio', 'Alberca Balarezo'),
(12, 'Consuelo Invonne', 'Del Castillo Castro'),
(13, 'Yesabella Katherine', 'Brenis Delgado'),
(14, 'Jose Fortunato', 'Zuloaga Cachay'),
(15, 'Jessie Leila', 'Bravo Jaico'),
(16, 'Maria Lourdes', 'Redondo Redondo'),
(17, 'Rony Rafael', 'Garcia Apestegui'),
(18, 'Mariana', 'Chavarry Chankay'),
(19, 'Doris Liliana', 'Moscol Mogollon'),
(20, 'Javier Alejandro', 'Huaman Angulo'),
(21, 'William Alfredo', 'Noblecilla Vinces'),
(22, 'Nancy Emilia', 'Estela Salazar'),
(23, 'Miguel Angel', 'Diaz Espino'),
(24, 'Segundo José', 'Castillo Zumarán'),
(25, 'Ernesto Ludwin', 'Nicho Cordova'),
(26, 'Claudia Emperatriz', 'Rodriguez Ortiz'),
(27, 'David Ysrael', 'Gonzales Lopez'),
(28, 'Fernando Pavel', 'Diaz Chero'),
(29, 'Martha Elizabeth', 'Chavez Alarcon'),
(30, 'Luis Orlando', 'Morante Adrianzen'),
(31, 'Luis', 'Saavedra Carrasco'),
(32, 'Karhy Estela', 'Cipriano Urtecho de Yong'),
(33, 'Jose Fernando', 'Quiroz Vidarte'),
(34, 'Jenny Patricia', 'Palacios Kuoc');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla grupo
--

CREATE TABLE grupo (
  id int(11) NOT NULL,
  denominacion char(1) NOT NULL,
  semestrecodigo char(6) NOT NULL,
  cursoid int(11) NOT NULL,
  docenteid int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla grupo
--

INSERT INTO grupo (id, denominacion, semestrecodigo, cursoid, docenteid) VALUES
(1, 'B', '2024-2', 2, 2),
(2, 'A', '2024-2', 1, 1),
(3, 'B', '2024-2', 6, 3),
(4, 'I', '2024-2', 4, 4),
(5, 'B', '2024-2', 5, 5),
(6, 'A', '2024-2', 3, 6),
(7, 'B', '2023-2', 29, 12),
(8, 'B', '2023-2', 8, 10),
(9, 'B', '2023-2', 10, 13),
(10, 'B', '2023-2', 30, 14),
(11, 'A', '2022-1', 11, 19),
(12, 'A', '2022-1', 12, 8),
(13, 'A', '2022-1', 15, 7),
(14, 'N', '2023-1', 26, 11),
(15, 'B', '2023-2', 31, 15),
(16, 'C', '2022-2', 17, 9),
(17, 'B', '2023-1', 24, 17),
(18, 'S', '2023-2', 9, 16),
(19, 'B', '2023-1', 23, 1),
(20, 'B', '2023-1', 28, 2),
(21, 'C', '2022-2', 21, 18),
(22, 'B', '2024-1', 33, 8),
(23, 'A', '2022-1', 13, 20),
(24, 'A', '2022-1', 14, 21),
(25, 'B', '2024-1', 37, 21),
(26, 'B', '2024-1', 36, 23),
(27, 'C', '2024-1', 35, 22),
(28, 'B', '2024-1', 34, 26),
(29, 'B', '2024-1', 32, 24),
(30, 'B', '2024-1', 7, 25),
(31, 'A', '2022-1', 16, 27),
(32, 'C', '2022-2', 18, 28),
(33, 'A', '2022-2', 19, 29),
(34, 'A', '2022-2', 20, 30),
(35, 'B', '2022-2', 22, 31),
(36, 'B', '2023-1', 25, 32),
(37, 'B', '2023-1', 27, 33),
(38, 'C', '2024-2', 38, 34);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla grupo_modelo
--

CREATE TABLE grupo_modelo (
  grupoid int(11) NOT NULL,
  modeloid int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla horario
--

CREATE TABLE horario (
  id int(10) NOT NULL,
  dia int(10) NOT NULL,
  h_inicio int(10) NOT NULL,
  h_final int(10) NOT NULL,
  grupoid int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla horario
--

INSERT INTO horario (id, dia, h_inicio, h_final, grupoid) VALUES
(1, 2, 20, 22, 1),
(2, 4, 15, 19, 1),
(3, 3, 18, 21, 2),
(4, 5, 18, 21, 2),
(5, 2, 16, 19, 4),
(6, 2, 9, 14, 6),
(7, 4, 13, 15, 3),
(8, 5, 15, 18, 3),
(9, 5, 13, 15, 5),
(10, 3, 15, 18, 5),
(11, 1, 8, 10, 7),
(12, 3, 8, 11, 7),
(13, 1, 10, 13, 8),
(14, 5, 15, 17, 8),
(15, 2, 13, 16, 9),
(16, 5, 17, 20, 9),
(17, 2, 16, 18, 10),
(18, 6, 10, 13, 10),
(19, 5, 10, 13, 18),
(20, 4, 16, 19, 15),
(21, 3, 11, 13, 15),
(22, 4, 9, 11, 38),
(23, 1, 8, 11, 36),
(24, 2, 8, 10, 36),
(25, 4, 16, 19, 14),
(26, 2, 10, 13, 20),
(27, 3, 7, 9, 20),
(28, 3, 10, 13, 37),
(29, 4, 9, 11, 37),
(30, 4, 7, 9, 19),
(31, 5, 7, 10, 19),
(32, 2, 14, 17, 17),
(33, 5, 10, 13, 17),
(34, 1, 7, 10, 22),
(35, 3, 11, 13, 22),
(36, 1, 10, 13, 27),
(37, 5, 7, 10, 30),
(38, 4, 10, 12, 30),
(39, 5, 10, 12, 29),
(40, 6, 10, 13, 29),
(41, 4, 7, 10, 25),
(42, 2, 7, 10, 28),
(43, 3, 9, 11, 28),
(44, 2, 10, 12, 26),
(45, 3, 7, 9, 26),
(46, 1, 7, 9, 33),
(47, 2, 11, 13, 33),
(48, 2, 7, 9, 34),
(49, 4, 7, 9, 34),
(50, 1, 10, 12, 21),
(51, 2, 16, 19, 21),
(52, 1, 16, 19, 35),
(53, 5, 17, 19, 35),
(54, 3, 14, 17, 16),
(55, 4, 13, 16, 16),
(56, 3, 17, 19, 32),
(57, 4, 16, 19, 32),
(58, 1, 7, 10, 11),
(59, 3, 7, 9, 11),
(60, 1, 10, 13, 12),
(61, 2, 15, 18, 23),
(62, 4, 15, 17, 23),
(63, 2, 10, 13, 24),
(64, 4, 9, 11, 24),
(65, 3, 11, 13, 13),
(66, 5, 7, 10, 13),
(67, 4, 11, 13, 31),
(68, 5, 10, 13, 31);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla matricula
--

CREATE TABLE matricula (
  id int(11) NOT NULL,
  alumnoid int(11) NOT NULL,
  semestrecodigo char(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla matricula
--

INSERT INTO matricula (id, alumnoid, semestrecodigo) VALUES
(1, 1, '2022-1'),
(2, 1, '2022-2'),
(3, 1, '2023-1'),
(4, 1, '2023-2'),
(5, 1, '2024-1'),
(6, 1, '2024-2'),
(7, 2, '2022-1'),
(8, 2, '2022-2'),
(9, 2, '2023-1'),
(10, 2, '2023-2'),
(11, 2, '2024-1'),
(12, 2, '2024-2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla modelo
--

CREATE TABLE modelo (
  id int(11) NOT NULL,
  nombre varchar(55) NOT NULL,
  alumnoid int(11) NOT NULL,
  semestrecodigo char(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla semestre
--

CREATE TABLE semestre (
  codigo char(6) NOT NULL,
  f_inicio date NOT NULL,
  f_final date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla semestre
--

INSERT INTO semestre (codigo, f_inicio, f_final) VALUES
('2022-1', '2024-12-31', '2024-12-31'),
('2022-2', '2024-12-31', '2024-12-31'),
('2023-1', '2024-12-31', '2024-12-31'),
('2023-2', '2024-12-31', '2024-12-31'),
('2024-1', '2024-12-31', '2024-12-31'),
('2024-2', '2024-12-31', '2024-12-31'),
('2025-1', '2024-12-16', '2024-12-25'),
('2025-2', '2024-12-10', '2024-12-24');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla alumno
--
ALTER TABLE alumno
  ADD PRIMARY KEY (id);

--
-- Indices de la tabla color
--
ALTER TABLE color
  ADD PRIMARY KEY (id);

--
-- Indices de la tabla curso
--
ALTER TABLE curso
  ADD PRIMARY KEY (id),
  ADD KEY FKcurso421515 (colorid);

--
-- Indices de la tabla curso_curso
--
ALTER TABLE curso_curso
  ADD PRIMARY KEY (cursoid,cursoid_pre),
  ADD KEY FKcurso_curs627155 (cursoid_pre);

--
-- Indices de la tabla detalles_matricula
--
ALTER TABLE detalles_matricula
  ADD PRIMARY KEY (grupoid,matriculaid),
  ADD KEY FKdetalles_m3019 (matriculaid);

--
-- Indices de la tabla docente
--
ALTER TABLE docente
  ADD PRIMARY KEY (id);

--
-- Indices de la tabla grupo
--
ALTER TABLE grupo
  ADD PRIMARY KEY (id),
  ADD KEY FKgrupo65739 (semestrecodigo),
  ADD KEY FKgrupo646143 (cursoid),
  ADD KEY FKgrupo55510 (docenteid);

--
-- Indices de la tabla grupo_modelo
--
ALTER TABLE grupo_modelo
  ADD PRIMARY KEY (grupoid,modeloid),
  ADD KEY FKgrupo_mode815667 (modeloid);

--
-- Indices de la tabla horario
--
ALTER TABLE horario
  ADD PRIMARY KEY (id),
  ADD KEY FKhorario682240 (grupoid);

--
-- Indices de la tabla matricula
--
ALTER TABLE matricula
  ADD PRIMARY KEY (id),
  ADD KEY FKmatricula928478 (alumnoid),
  ADD KEY FKmatricula699956 (semestrecodigo);

--
-- Indices de la tabla modelo
--
ALTER TABLE modelo
  ADD PRIMARY KEY (id),
  ADD KEY FKmodelo712826 (alumnoid),
  ADD KEY FKmodelo630328 (semestrecodigo);

--
-- Indices de la tabla semestre
--
ALTER TABLE semestre
  ADD PRIMARY KEY (codigo);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla alumno
--
ALTER TABLE alumno
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla color
--
ALTER TABLE color
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla curso
--
ALTER TABLE curso
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT de la tabla docente
--
ALTER TABLE docente
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla grupo
--
ALTER TABLE grupo
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla horario
--
ALTER TABLE horario
  MODIFY id int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT de la tabla matricula
--
ALTER TABLE matricula
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla modelo
--
ALTER TABLE modelo
  MODIFY id int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla curso
--
ALTER TABLE curso
  ADD CONSTRAINT FKcurso421515 FOREIGN KEY (colorid) REFERENCES color (id);

--
-- Filtros para la tabla curso_curso
--
ALTER TABLE curso_curso
  ADD CONSTRAINT FKcurso_curs627155 FOREIGN KEY (cursoid_pre) REFERENCES curso (id),
  ADD CONSTRAINT FKcurso_curs955408 FOREIGN KEY (cursoid) REFERENCES curso (id);

--
-- Filtros para la tabla detalles_matricula
--
ALTER TABLE detalles_matricula
  ADD CONSTRAINT FKdetalles_m3019 FOREIGN KEY (matriculaid) REFERENCES matricula (id),
  ADD CONSTRAINT FKdetalles_m96921 FOREIGN KEY (grupoid) REFERENCES grupo (id);

--
-- Filtros para la tabla grupo
--
ALTER TABLE grupo
  ADD CONSTRAINT FKgrupo55510 FOREIGN KEY (docenteid) REFERENCES docente (id),
  ADD CONSTRAINT FKgrupo646143 FOREIGN KEY (cursoid) REFERENCES curso (id),
  ADD CONSTRAINT FKgrupo65739 FOREIGN KEY (semestrecodigo) REFERENCES semestre (codigo);

--
-- Filtros para la tabla grupo_modelo
--
ALTER TABLE grupo_modelo
  ADD CONSTRAINT FKgrupo_mode463927 FOREIGN KEY (grupoid) REFERENCES grupo (id),
  ADD CONSTRAINT FKgrupo_mode815667 FOREIGN KEY (modeloid) REFERENCES modelo (id);

--
-- Filtros para la tabla horario
--
ALTER TABLE horario
  ADD CONSTRAINT FKhorario682240 FOREIGN KEY (grupoid) REFERENCES grupo (id);

--
-- Filtros para la tabla matricula
--
ALTER TABLE matricula
  ADD CONSTRAINT FKmatricula699956 FOREIGN KEY (semestrecodigo) REFERENCES semestre (codigo),
  ADD CONSTRAINT FKmatricula928478 FOREIGN KEY (alumnoid) REFERENCES alumno (id);

--
-- Filtros para la tabla modelo
--
ALTER TABLE modelo
  ADD CONSTRAINT FKmodelo630328 FOREIGN KEY (semestrecodigo) REFERENCES semestre (codigo),
  ADD CONSTRAINT FKmodelo712826 FOREIGN KEY (alumnoid) REFERENCES alumno (id);
COMMIT;
