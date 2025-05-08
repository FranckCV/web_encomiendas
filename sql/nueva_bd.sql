CREATE TABLE sucursal (
  id           int(10) NOT NULL AUTO_INCREMENT, 
  direccion    varchar(150) NOT NULL, 
  ubigeocodigo varchar(10) NOT NULL, 
  horario_l_v  varchar(255), 
  horario_s_d  varchar(255), 
  latitud      numeric(9, 6), 
  longitud     numeric(9, 6), 
  teléfono     char(255), 
  referencia   varchar(255), 
  activo       tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE transaccion_encomienda (
  num_serie          int(11) NOT NULL, 
  masivo             tinyint(1) NOT NULL comment ' 1 si es envío masivo
0 si es un empaque (paquete o sobre)
 ', 
  descripcion        varchar(255) NOT NULL, 
  monto_total        numeric(9, 6), 
  recojo_casa        tinyint(1) NOT NULL, 
  tipo_comprobanteid int(10) NOT NULL, 
  id_sucursal_origen int(11) NOT NULL, 
  fecha              date NOT NULL, 
  hora               time NOT NULL, 
  clienteid          int(10) NOT NULL, 
  PRIMARY KEY (num_serie, 
  tipo_comprobanteid));
CREATE TABLE estado_encomienda (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(50) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE cliente (
  usuarioid        int(10) NOT NULL AUTO_INCREMENT, 
  correo           varchar(150) NOT NULL UNIQUE, 
  telefono         varchar(15), 
  num_documento    varchar(20) NOT NULL, 
  nombre_siglas    varchar(150) NOT NULL, 
  apellidos_razon  varchar(150) NOT NULL, 
  tipo_documentoid int(11) NOT NULL, 
  tipo_clienteid   int(11) NOT NULL, 
  PRIMARY KEY (usuarioid));
CREATE TABLE tipo_unidad (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(20) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE articulo (
  id            int(10) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(100) NOT NULL, 
  precio        numeric(9, 6) NOT NULL, 
  stock         int(11) NOT NULL, 
  activo        tinyint(1) NOT NULL, 
  tamaño_cajaid int(11), 
  img           mediumblob NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE salida (
  id       int(10) NOT NULL AUTO_INCREMENT, 
  unidadid int(10) NOT NULL, 
  fecha    date NOT NULL, 
  hora     time NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_rol (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(150) NOT NULL, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  descripcion varchar(255), 
  PRIMARY KEY (id));
CREATE TABLE unidad (
  id            int(10) NOT NULL AUTO_INCREMENT, 
  placa         char(6) NOT NULL UNIQUE, 
  capacidad     numeric(9, 2) NOT NULL, 
  volumen       numeric(9, 2) NOT NULL, 
  observaciones text, 
  estado        char(1) NOT NULL, 
  modeloid      int(11) NOT NULL, 
  MTC           char(9) NOT NULL UNIQUE, 
  TUC           char(12) NOT NULL UNIQUE, 
  PRIMARY KEY (id));
CREATE TABLE ubigeo (
  codigo       varchar(10) NOT NULL, 
  departamento varchar(150) NOT NULL, 
  provincia    varchar(150) NOT NULL, 
  distrito     varchar(150) NOT NULL, 
  activo       tinyint(1) NOT NULL, 
  PRIMARY KEY (codigo));
CREATE TABLE empleado (
  usuarioid int(10) NOT NULL AUTO_INCREMENT, 
  nombre    varchar(150) NOT NULL, 
  apellidos varchar(150) NOT NULL, 
  rolid     int(11) NOT NULL, 
  PRIMARY KEY (usuarioid));
CREATE TABLE escalas (
  sucursalid int(10) NOT NULL, 
  salidaid   int(10) NOT NULL, 
  PRIMARY KEY (sucursalid, 
  salidaid));
CREATE TABLE empleado_salida (
  salidaid          int(10) NOT NULL, 
  empleadousuarioid int(10) NOT NULL, 
  PRIMARY KEY (salidaid, 
  empleadousuarioid));
CREATE TABLE seguimiento (
  estado_encomiendaid int(10) NOT NULL, 
  paquetetracking     int(11) NOT NULL, 
  PRIMARY KEY (estado_encomiendaid, 
  paquetetracking));
CREATE TABLE transaccion_venta (
  transaccionnum_serie int(11) NOT NULL, 
  tipo_comprobanteid   int(10) NOT NULL, 
  monto_total          numeric(9, 6), 
  fecha                date NOT NULL, 
  hora                 time NOT NULL, 
  clienteid            int(10) NOT NULL, 
  PRIMARY KEY (transaccionnum_serie, 
  tipo_comprobanteid));
CREATE TABLE detalle_venta (
  articuloid                int(10) NOT NULL, 
  cantidad                  int(10) NOT NULL, 
  ventatransaccionnum_serie int(11) NOT NULL, 
  ventatipo_comprobanteid   int(10) NOT NULL, 
  PRIMARY KEY (articuloid, 
  ventatransaccionnum_serie, 
  ventatipo_comprobanteid));
CREATE TABLE reclamo (
  estado_reclamoid     int(10) NOT NULL, 
  id                   int(10) NOT NULL AUTO_INCREMENT, 
  tipo_indemnizacionid int(10), 
  monto_indemnizado    numeric(9, 6), 
  paquetetracking      int(11) NOT NULL, 
  clienteid            int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE estado_reclamo (
  id     int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_indemnizacion (
  id     int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(150) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_comprobante (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      char(1) NOT NULL, 
  descripcion varchar(255) NOT NULL, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  inicial     char(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE marca (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(20) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE modelo (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(20) NOT NULL, 
  activo        tinyint(1) NOT NULL, 
  marcaid       int(11) NOT NULL, 
  tipo_unidadid int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE rol (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(100) NOT NULL, 
  descripcion varchar(150) NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  tipo_rolid  int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE metodo_pago (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE metodo_pago_venta (
  id               int(11) NOT NULL AUTO_INCREMENT, 
  metodo_pagoid    int(11) NOT NULL, 
  num_serie        int(11) NOT NULL, 
  tipo_comprobante int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_paquete (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(150) NOT NULL comment ' 
ACCESORIOS PARA FIESTAS
ACCESORIOS ELECTRÓNICOS
ARTÍCULOS DE LIMPIEZA
ARTÍCULOS PUBLICITARIOS
BISUTERIA
CAJA
TARJETAS PERSONALES
MUEBLES Y DECOHOGAR
FERRETERÍA Y CONSTRUCCIÓN
ALIMENTACION Y BEBIDAS
COSMETICOS
ELECTROHOGAR
JUGUETES
MATERIAL MEDICO
MEDICINAS
REPUESTOS
ROPA Y ACCESORIOS
VALIJA-DOCUMENTOS
UTILES DE ESCRITORIO
UTILES DE OFICINA
 ', 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_documento (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(50) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE encomienda (
  tracking                                  int(11) NOT NULL AUTO_INCREMENT, 
  valor                                     numeric(9, 6) NOT NULL, 
  peso                                      numeric(9, 6) NOT NULL, 
  alto                                      numeric(9, 6) NOT NULL, 
  largo                                     numeric(9, 6) NOT NULL, 
  ancho                                     numeric(9, 6) NOT NULL, 
  descripcion                               varchar(255) NOT NULL, 
  direccion_destinatario                    varchar(255), 
  num_documento_destinatario                int(11), 
  tipo_documento_destinatario_id            int(11) NOT NULL, 
  telefono_destinatario                     int(11), 
  tipo_empaque                              char(1) NOT NULL comment 'P : Paquete
S: Sobre
 ', 
  tipo_paqueteid                            int(11) NOT NULL, 
  tipo_recojoid                             int(11) NOT NULL, 
  salidaid                                  int(10) NOT NULL, 
  transaccion_encomienda_num_serie          int(11), 
  transaccion_encomienda_tipo_comprobanteid int(10), 
  PRIMARY KEY (tracking));
CREATE TABLE tamaño_caja (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(3) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_recojo (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL comment 'Recojo en tienda
Envío a domicilio
Con recojo y pago en tienda
 ', 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tarifa_ruta (
  tarifa              numeric(9, 6) NOT NULL, 
  sucursal_origen_id  int(10) NOT NULL, 
  sucursal_destino_id int(10) NOT NULL, 
  PRIMARY KEY (sucursal_origen_id, 
  sucursal_destino_id));
CREATE TABLE modulo (
  id       int(11) NOT NULL AUTO_INCREMENT, 
  `Column` int(11), 
  PRIMARY KEY (id));
CREATE TABLE pagina (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  `Column`      int(11), 
  tipo_paginaid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE acceso (
  paginaid int(11) NOT NULL, 
  moduloid int(11) NOT NULL, 
  PRIMARY KEY (paginaid, 
  moduloid));
CREATE TABLE tipo_pagina (
  id int(11) NOT NULL AUTO_INCREMENT, 
  PRIMARY KEY (id));
CREATE TABLE usuario (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  correo      varchar(255) NOT NULL UNIQUE, 
  contrasenia varchar(255) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_cliente (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE empresa (
  id         int(11) NOT NULL AUTO_INCREMENT, 
  nombre     varchar(200) NOT NULL, 
  correo     int(11) NOT NULL, 
  ruc        char(11) NOT NULL, 
  logo       mediumblob NOT NULL, 
  imagenesid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE redes (
  id        int(11) NOT NULL AUTO_INCREMENT, 
  nombre    varchar(150) NOT NULL, 
  enlace    text NOT NULL, 
  icono     text NOT NULL, 
  empresaid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE imagenes (
  id   int(11) NOT NULL AUTO_INCREMENT, 
  ruta text NOT NULL, 
  PRIMARY KEY (id));
ALTER TABLE sucursal ADD CONSTRAINT FKsucursal756715 FOREIGN KEY (ubigeocodigo) REFERENCES ubigeo (codigo);
ALTER TABLE escalas ADD CONSTRAINT FKescalas126327 FOREIGN KEY (sucursalid) REFERENCES sucursal (id);
ALTER TABLE escalas ADD CONSTRAINT FKescalas109658 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s308635 FOREIGN KEY (empleadousuarioid) REFERENCES empleado (usuarioid);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s707218 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE salida ADD CONSTRAINT FKsalida314397 FOREIGN KEY (unidadid) REFERENCES unidad (id);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient857034 FOREIGN KEY (estado_encomiendaid) REFERENCES estado_encomienda (id);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve532256 FOREIGN KEY (articuloid) REFERENCES articulo (id);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve352841 FOREIGN KEY (ventatransaccionnum_serie, ventatipo_comprobanteid) REFERENCES transaccion_venta (transaccionnum_serie, tipo_comprobanteid);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo902505 FOREIGN KEY (estado_reclamoid) REFERENCES estado_reclamo (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo501927 FOREIGN KEY (tipo_indemnizacionid) REFERENCES tipo_indemnizacion (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo121578 FOREIGN KEY (marcaid) REFERENCES marca (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo83299 FOREIGN KEY (tipo_unidadid) REFERENCES tipo_unidad (id);
ALTER TABLE unidad ADD CONSTRAINT FKunidad608127 FOREIGN KEY (modeloid) REFERENCES modelo (id);
ALTER TABLE metodo_pago_venta ADD CONSTRAINT FKmetodo_pag702897 FOREIGN KEY (metodo_pagoid) REFERENCES metodo_pago (id);
ALTER TABLE encomienda ADD CONSTRAINT FKencomienda197360 FOREIGN KEY (transaccion_encomienda_num_serie, transaccion_encomienda_tipo_comprobanteid) REFERENCES transaccion_encomienda (num_serie, tipo_comprobanteid);
ALTER TABLE empleado ADD CONSTRAINT FKempleado961716 FOREIGN KEY (rolid) REFERENCES rol (id);
ALTER TABLE articulo ADD CONSTRAINT FKarticulo75124 FOREIGN KEY (tamaño_cajaid) REFERENCES tamaño_caja (id);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient816604 FOREIGN KEY (paquetetracking) REFERENCES encomienda (tracking);
ALTER TABLE encomienda ADD CONSTRAINT FKencomienda483113 FOREIGN KEY (tipo_recojoid) REFERENCES tipo_recojo (id);
ALTER TABLE encomienda ADD CONSTRAINT FKencomienda889660 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE encomienda ADD CONSTRAINT FKencomienda794220 FOREIGN KEY (tipo_documento_destinatario_id) REFERENCES tipo_documento (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut972797 FOREIGN KEY (sucursal_origen_id) REFERENCES sucursal (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut28234 FOREIGN KEY (sucursal_destino_id) REFERENCES sucursal (id);
ALTER TABLE rol ADD CONSTRAINT FKrol677440 FOREIGN KEY (tipo_rolid) REFERENCES tipo_rol (id);
ALTER TABLE cliente ADD CONSTRAINT FKcliente66106 FOREIGN KEY (tipo_documentoid) REFERENCES tipo_documento (id);
ALTER TABLE encomienda ADD CONSTRAINT FKencomienda625453 FOREIGN KEY (tipo_paqueteid) REFERENCES tipo_paquete (id);
ALTER TABLE acceso ADD CONSTRAINT FKacceso288305 FOREIGN KEY (paginaid) REFERENCES pagina (id);
ALTER TABLE acceso ADD CONSTRAINT FKacceso480304 FOREIGN KEY (moduloid) REFERENCES modulo (id);
ALTER TABLE pagina ADD CONSTRAINT FKpagina910561 FOREIGN KEY (tipo_paginaid) REFERENCES tipo_pagina (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo878971 FOREIGN KEY (paquetetracking) REFERENCES encomienda (tracking);
ALTER TABLE transaccion_encomienda ADD CONSTRAINT FKtransaccio662746 FOREIGN KEY (tipo_comprobanteid) REFERENCES tipo_comprobante (id);
ALTER TABLE transaccion_venta ADD CONSTRAINT FKtransaccio293973 FOREIGN KEY (tipo_comprobanteid) REFERENCES tipo_comprobante (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo210055 FOREIGN KEY (clienteid) REFERENCES cliente (usuarioid);
ALTER TABLE cliente ADD CONSTRAINT FKcliente404372 FOREIGN KEY (tipo_clienteid) REFERENCES tipo_cliente (id);
ALTER TABLE redes ADD CONSTRAINT FKredes671243 FOREIGN KEY (empresaid) REFERENCES empresa (id);
ALTER TABLE empresa ADD CONSTRAINT FKempresa125247 FOREIGN KEY (imagenesid) REFERENCES imagenes (id);
ALTER TABLE transaccion_encomienda ADD CONSTRAINT FKtransaccio902557 FOREIGN KEY (clienteid) REFERENCES cliente (usuarioid);
ALTER TABLE transaccion_venta ADD CONSTRAINT FKtransaccio533784 FOREIGN KEY (clienteid) REFERENCES cliente (usuarioid);
