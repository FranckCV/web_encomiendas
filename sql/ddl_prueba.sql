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
  transaccionnum_serie          int(11) NOT NULL, 
  transacciontipo_comprobanteid int(10) NOT NULL, 
  sucursal_origen_id            int(10) NOT NULL, 
  masivo                        tinyint(1) NOT NULL, 
  descripcion                   varchar(255) NOT NULL, 
  monto_total                   numeric(9, 6), 
  recojo_casa                   tinyint(1) NOT NULL, 
  PRIMARY KEY (transaccionnum_serie, 
  transacciontipo_comprobanteid));
CREATE TABLE estado_encomienda (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(50) NOT NULL, 
  descripción text NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE usuario (
  id               int(10) NOT NULL AUTO_INCREMENT, 
  correo           varchar(150) NOT NULL UNIQUE, 
  contraseña       varchar(150) NOT NULL, 
  activo           tinyint(1) NOT NULL, 
  telefono         varchar(15), 
  tipo_usuario     char(2) NOT NULL , 
  num_documento    varchar(20) NOT NULL, 
  tipo_documentoid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_unidad (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(20) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE articulo (
  id            int(10) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(100) NOT NULL, 
  precio        numeric(9, 6) NOT NULL, 
  stock         int(11) NOT NULL, 
  activo        tinyint(1) NOT NULL, 
  tamaño_cajaid int(11), 
  PRIMARY KEY (id));
CREATE TABLE salida (
  id       int(10) NOT NULL AUTO_INCREMENT, 
  unidadid int(10) NOT NULL, 
  fecha    date NOT NULL, 
  hora     time NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_cargo (
  id     int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(150) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE unidad (
  id                int(10) NOT NULL AUTO_INCREMENT, 
  placa             varchar(10) NOT NULL UNIQUE, 
  capacidad         numeric(9, 2) NOT NULL, 
  volumen           numeric(9, 2) NOT NULL, 
  observaciones     text, 
  estado            char(1) NOT NULL, 
  modeloid          int(11) NOT NULL, 
  sucursal_actualid int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE ubigeo (
  codigo       varchar(10) NOT NULL, 
  departamento varchar(150) NOT NULL, 
  provincia    varchar(150) NOT NULL, 
  distrito     varchar(150) NOT NULL, 
  activo       tinyint(1) NOT NULL, 
  PRIMARY KEY (codigo));
CREATE TABLE empleado (
  usuarioid   int(10) NOT NULL, 
  nombre      varchar(150) NOT NULL, 
  ape_paterno varchar(150) NOT NULL, 
  ape_materno varchar(150) NOT NULL, 
  cargoid     int(11) NOT NULL, 
  PRIMARY KEY (usuarioid));
CREATE TABLE persona_natural (
  usuarioid   int(10) NOT NULL, 
  nombre      int(11) NOT NULL, 
  ape_paterno int(11) NOT NULL, 
  ape_materno varchar(150) NOT NULL, 
  PRIMARY KEY (usuarioid));
CREATE TABLE juridica (
  usuarioid    int(10) NOT NULL, 
  razon_social varchar(150) NOT NULL, 
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
CREATE TABLE venta (
  monto_total                   numeric(9, 6), 
  transaccionnum_serie          int(11) NOT NULL, 
  transacciontipo_comprobanteid int(10) NOT NULL, 
  PRIMARY KEY (transaccionnum_serie, 
  transacciontipo_comprobanteid));
CREATE TABLE detalle_venta (
  articuloid                         int(10) NOT NULL, 
  cantidad                           int(10) NOT NULL, 
  ventatransacciontipo_comprobanteid int(10) NOT NULL, 
  ventatransaccionnum_serie          int(11) NOT NULL, 
  PRIMARY KEY (articuloid, 
  ventatransacciontipo_comprobanteid, 
  ventatransaccionnum_serie));
CREATE TABLE reclamo (
  estado_reclamoid                                    int(10) NOT NULL, 
  id                                                  int(10) NOT NULL AUTO_INCREMENT, 
  indemnizacionid                                     int(10), 
  transaccion_encomiendatransaccionnum_serie          int(11), 
  transaccion_encomiendatransacciontipo_comprobanteid int(10), 
  usuarioid                                           int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE estado_reclamo (
  id     int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_indemnizacion (
  id                int(10) NOT NULL AUTO_INCREMENT, 
  nombre            varchar(150) NOT NULL, 
  monto_indemnizado numeric(9, 6) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_comprobante (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      char(1) NOT NULL, 
  descripcion varchar(100) NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE marca (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(20) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE modelo (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(20) NOT NULL, 
  marcaid       int(11) NOT NULL, 
  tipo_unidadid int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE cargo (
  id           int(11) NOT NULL AUTO_INCREMENT, 
  nombre       varchar(100) NOT NULL, 
  activo       tinyint(1) NOT NULL, 
  descripcion  varchar(150) NOT NULL, 
  tipo_cargoid int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE metodo_pago (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE metodos_venta (
  id                            int(11) NOT NULL AUTO_INCREMENT, 
  metodo_pagoid                 int(11) NOT NULL, 
  transaccionnum_serie          int(11) NOT NULL, 
  transacciontipo_comprobanteid int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_paquete (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(150) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_documento (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(50) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE paquete (
  tracking                                            int(11) NOT NULL AUTO_INCREMENT, 
  valor                                               numeric(9, 6) NOT NULL, 
  peso                                                numeric(9, 6) NOT NULL, 
  alto                                                numeric(9, 6) NOT NULL, 
  largo                                               numeric(9, 6) NOT NULL, 
  ancho                                               numeric(9, 6) NOT NULL, 
  descripcion                                         varchar(255) NOT NULL, 
  direccion                                           varchar(255) NOT NULL, 
  destino                                             int(11) NOT NULL, 
  transaccion_encomiendanum_serie                     char(11) NOT NULL, 
  transaccion_encomiendatipo_comprobanteid            int(10) NOT NULL, 
  adquirenteNum_documento                             int(11) NOT NULL, 
  num_documento_destinatario                          int(11), 
  telefono_destinatario                               int(11), 
  tipo_empaque                                        char(1) NOT NULL, 
  tipo_paqueteid                                      int(11) NOT NULL, 
  tipo_recojoid                                       int(11) NOT NULL, 
  salidaid                                            int(10) NOT NULL, 
  tipo_documento_destinatario_id                      int(11) NOT NULL, 
  transaccion_encomiendatransaccionnum_serie          int(11), 
  transaccion_encomiendatransacciontipo_comprobanteid int(10), 
  PRIMARY KEY (tracking));
CREATE TABLE tamaño_caja (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(3) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_recojo (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE transaccion (
  num_serie          int(11) NOT NULL, 
  fecha              date NOT NULL, 
  hora               time NOT NULL, 
  tipo_comprobanteid int(10) NOT NULL, 
  PRIMARY KEY (num_serie, 
  tipo_comprobanteid));
CREATE TABLE tarifa_ruta (
  tarifa              numeric(9, 6) NOT NULL, 
  sucursal_origen_id  int(10) NOT NULL, 
  sucursal_destino_id int(10) NOT NULL, 
  PRIMARY KEY (sucursal_origen_id, 
  sucursal_destino_id));

ALTER TABLE sucursal ADD CONSTRAINT FKsucursal756715 FOREIGN KEY (ubigeocodigo) REFERENCES ubigeo (codigo);
ALTER TABLE escalas ADD CONSTRAINT FKescalas126327 FOREIGN KEY (sucursalid) REFERENCES sucursal (id);
ALTER TABLE escalas ADD CONSTRAINT FKescalas109658 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s308635 FOREIGN KEY (empleadousuarioid) REFERENCES empleado (usuarioid);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s707218 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE salida ADD CONSTRAINT FKsalida314397 FOREIGN KEY (unidadid) REFERENCES unidad (id);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient857034 FOREIGN KEY (estado_encomiendaid) REFERENCES estado_encomienda (id);
ALTER TABLE transaccion_encomienda ADD CONSTRAINT FKtransaccio607509 FOREIGN KEY (sucursal_origen_id) REFERENCES sucursal (id);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve532256 FOREIGN KEY (articuloid) REFERENCES articulo (id);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve887719 FOREIGN KEY (ventatransaccionnum_serie, ventatransacciontipo_comprobanteid) REFERENCES venta (transaccionnum_serie, transacciontipo_comprobanteid);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo902505 FOREIGN KEY (estado_reclamoid) REFERENCES estado_reclamo (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo244422 FOREIGN KEY (indemnizacionid) REFERENCES tipo_indemnizacion (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo606747 FOREIGN KEY (transaccion_encomiendatransaccionnum_serie, transaccion_encomiendatransacciontipo_comprobanteid) REFERENCES transaccion_encomienda (transaccionnum_serie, transacciontipo_comprobanteid);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo121578 FOREIGN KEY (marcaid) REFERENCES marca (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo83299 FOREIGN KEY (tipo_unidadid) REFERENCES tipo_unidad (id);
ALTER TABLE unidad ADD CONSTRAINT FKunidad608127 FOREIGN KEY (modeloid) REFERENCES modelo (id);
ALTER TABLE metodos_venta ADD CONSTRAINT FKmetodos_ve840843 FOREIGN KEY (metodo_pagoid) REFERENCES metodo_pago (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete717630 FOREIGN KEY (transaccion_encomiendatransaccionnum_serie, transaccion_encomiendatransacciontipo_comprobanteid) REFERENCES transaccion_encomienda (transaccionnum_serie, transacciontipo_comprobanteid);
ALTER TABLE empleado ADD CONSTRAINT FKempleado623722 FOREIGN KEY (cargoid) REFERENCES cargo (id);
ALTER TABLE articulo ADD CONSTRAINT FKarticulo75124 FOREIGN KEY (tamaño_cajaid) REFERENCES tamaño_caja (id);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient381900 FOREIGN KEY (paquetetracking) REFERENCES paquete (tracking);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete715391 FOREIGN KEY (tipo_recojoid) REFERENCES tipo_recojo (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete691155 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete992725 FOREIGN KEY (tipo_documento_destinatario_id) REFERENCES tipo_documento (id);
ALTER TABLE transaccion_encomienda ADD CONSTRAINT FKtransaccio288128 FOREIGN KEY (transaccionnum_serie, transacciontipo_comprobanteid) REFERENCES transaccion (num_serie, tipo_comprobanteid);
ALTER TABLE transaccion ADD CONSTRAINT FKtransaccio752056 FOREIGN KEY (tipo_comprobanteid) REFERENCES tipo_comprobante (id);
ALTER TABLE venta ADD CONSTRAINT FKventa379324 FOREIGN KEY (transaccionnum_serie, transacciontipo_comprobanteid) REFERENCES transaccion (num_serie, tipo_comprobanteid);
ALTER TABLE metodos_venta ADD CONSTRAINT FKmetodos_ve128016 FOREIGN KEY (transaccionnum_serie, transacciontipo_comprobanteid) REFERENCES transaccion (num_serie, tipo_comprobanteid);
ALTER TABLE unidad ADD CONSTRAINT FKunidad749055 FOREIGN KEY (sucursal_actualid) REFERENCES sucursal (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut972797 FOREIGN KEY (sucursal_origen_id) REFERENCES sucursal (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut28234 FOREIGN KEY (sucursal_destino_id) REFERENCES sucursal (id);
ALTER TABLE cargo ADD CONSTRAINT FKcargo330823 FOREIGN KEY (tipo_cargoid) REFERENCES tipo_cargo (id);
ALTER TABLE empleado ADD CONSTRAINT FKempleado448484 FOREIGN KEY (usuarioid) REFERENCES usuario (id);
ALTER TABLE usuario ADD CONSTRAINT FKusuario632844 FOREIGN KEY (tipo_documentoid) REFERENCES tipo_documento (id);
ALTER TABLE juridica ADD CONSTRAINT FKjuridica199325 FOREIGN KEY (usuarioid) REFERENCES usuario (id);
ALTER TABLE persona_natural ADD CONSTRAINT FKnatural685166 FOREIGN KEY (usuarioid) REFERENCES usuario (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo865871 FOREIGN KEY (usuarioid) REFERENCES usuario (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete426948 FOREIGN KEY (tipo_paqueteid) REFERENCES tipo_paquete (id);
