CREATE TABLE transaccion_encomienda (
  num_serie          int(11) NOT NULL AUTO_INCREMENT, 
  masivo             tinyint(1) NOT NULL comment ' 1 si es envío masivo
0 si es un empaque (paquete o sobre)
 ', 
  descripcion        text NOT NULL, 
  monto_total        numeric(9, 2), 
  recojo_casa        tinyint(1) NOT NULL, 
  id_sucursal_origen int(11) NOT NULL, 
  fecha              date NOT NULL, 
  hora               time NOT NULL, 
  clienteid          int(10) NOT NULL, 
  tipo_comprobanteid int(10) NOT NULL, 
  PRIMARY KEY (num_serie));
CREATE TABLE detalle_estado (
  id                  int(10) NOT NULL AUTO_INCREMENT, 
  nombre              varchar(50) NOT NULL, 
  descripcion         text, 
  activo              tinyint(1) DEFAULT 1 NOT NULL, 
  estado_encomiendaid int(4) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE cliente (
  usuarioid        int(10) NOT NULL AUTO_INCREMENT, 
  correo           varchar(150) NOT NULL UNIQUE, 
  telefono         varchar(15), 
  num_documento    varchar(20) NOT NULL UNIQUE, 
  nombre_siglas    varchar(150) NOT NULL, 
  apellidos_razon  varchar(150) NOT NULL, 
  tipo_documentoid int(11) NOT NULL, 
  tipo_clienteid   int(11) NOT NULL, 
  PRIMARY KEY (usuarioid));
CREATE TABLE tipo_unidad (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(20) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE articulo (
  id            int(10) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(100) NOT NULL, 
  precio        numeric(9, 2) NOT NULL, 
  stock         int(11) NOT NULL, 
  activo        tinyint(1) NOT NULL, 
  img           mediumblob NOT NULL, 
  dimensiones   varchar(20), 
  tamaño_cajaid int(11), 
  PRIMARY KEY (id));
CREATE TABLE salida (
  id       int(10) NOT NULL AUTO_INCREMENT, 
  unidadid int(10) NOT NULL, 
  fecha    date NOT NULL, 
  hora     time NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_rol (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(250) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE unidad (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  placa       varchar(8) NOT NULL UNIQUE, 
  MTC         char(9) NOT NULL UNIQUE, 
  TUC         char(12) NOT NULL UNIQUE, 
  capacidad   numeric(9, 2) NOT NULL, 
  volumen     numeric(9, 2) NOT NULL, 
  descripcion text, 
  estado      char(1) NOT NULL, 
  modeloid    int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE ubigeo (
  codigo       varchar(10) NOT NULL, 
  departamento varchar(150) NOT NULL, 
  provincia    varchar(150) NOT NULL, 
  distrito     varchar(150) NOT NULL, 
  activo       tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (codigo));
CREATE TABLE empleado (
  usuarioid int(10) NOT NULL AUTO_INCREMENT, 
  nombre    varchar(150) NOT NULL, 
  apellidos varchar(150) NOT NULL, 
  correo    varchar(250) NOT NULL UNIQUE, 
  rolid     int(11) NOT NULL, 
  PRIMARY KEY (usuarioid));
CREATE TABLE escala (
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
  num_serie          int(11) NOT NULL, 
  tipo_comprobanteid int(10) NOT NULL, 
  monto_total        numeric(9, 2), 
  fecha              date NOT NULL, 
  hora               time NOT NULL, 
  clienteid          int(10) NOT NULL, 
  PRIMARY KEY (num_serie, 
  tipo_comprobanteid));
CREATE TABLE detalle_venta (
  articuloid              int(10) NOT NULL, 
  ventanum_serie          int(11) NOT NULL, 
  ventatipo_comprobanteid int(10) NOT NULL, 
  cantidad                int(10) NOT NULL, 
  PRIMARY KEY (articuloid, 
  ventanum_serie, 
  ventatipo_comprobanteid));
CREATE TABLE reclamo (
  id                   int(10) NOT NULL AUTO_INCREMENT, 
  nombres_razon        varchar(200) NOT NULL, 
  direccion            text NOT NULL, 
  correo               varchar(200) NOT NULL, 
  telefono             char(9) NOT NULL, 
  n_documento          varchar(11) NOT NULL, 
  monto_indemnizado    numeric(9, 2), 
  titulo_incidencia    varchar(150) NOT NULL, 
  bien_contratado      char(1) NOT NULL comment 'Producto (P)
Servicio (S)
 ', 
  monto_reclamado      numeric(9, 2) NOT NULL, 
  relacion             char(1) NOT NULL comment 'Quien envía
Quien recibe
 ', 
  fecha_recojo         date NOT NULL, 
  sucursal_id          int(11) NOT NULL, 
  descripcion          text NOT NULL, 
  pedido               text NOT NULL, 
  causa_reclamoid      int(11) NOT NULL, 
  estado_reclamoid     int(10) NOT NULL, 
  tipo_indemnizacionid int(10), 
  paquetetracking      int(11) NOT NULL, 
  ubigeocodigo         varchar(10) NOT NULL, 
  tipo_documentoid     int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE estado_reclamo (
  id     int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_indemnizacion (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(150) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_comprobante (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  inicial     varchar(3) NOT NULL, 
  nombre      varchar(50) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
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
  nombre      varchar(250) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  tipo_rolid  int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE metodo_pago (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE metodo_pago_venta (
  id               int(11) NOT NULL AUTO_INCREMENT, 
  num_serie        int(11) NOT NULL, 
  tipo_comprobante int(11) NOT NULL, 
  metodo_pagoid    int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE contenido_paquete (
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
  siglas char(3) NOT NULL, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE paquete (
  tracking                         int(11) NOT NULL AUTO_INCREMENT, 
  clave                            char(4) NOT NULL, 
  valor                            numeric(9, 2) NOT NULL, 
  peso                             numeric(9, 2) NOT NULL, 
  alto                             numeric(9, 2) NOT NULL, 
  largo                            numeric(9, 2) NOT NULL, 
  precio_ruta                      numeric(9, 2) NOT NULL, 
  ancho                            numeric(9, 2) NOT NULL, 
  descripcion                      text NOT NULL, 
  direccion_destinatario           varchar(255), 
  telefono_destinatario            varchar(20), 
  num_documento_destinatario       varchar(25), 
  sucursal_destino_id              int(11) NOT NULL, 
  codigo_postal                    char(5) NOT NULL, 
  tipo_documento_destinatario_id   int(11) NOT NULL, 
  contenido_paqueteid              int(11) NOT NULL, 
  tipo_recepcionid                 int(11) NOT NULL, 
  salidaid                         int(10) NOT NULL, 
  transaccion_encomienda_num_serie int(11), 
  tipo_empaqueid                   int(11) NOT NULL, 
  PRIMARY KEY (tracking));
CREATE TABLE tamanio_caja (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(3) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_recepcion (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL comment 'Recojo en tienda
Envío a domicilio
Con recojo y pago en tienda
 ', 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tarifa_ruta (
  sucursal_origen_id  int(10) NOT NULL, 
  sucursal_destino_id int(10) NOT NULL, 
  tarifa              numeric(9, 2) NOT NULL, 
  PRIMARY KEY (sucursal_origen_id, 
  sucursal_destino_id));
CREATE TABLE modulo (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(150) NOT NULL, 
  icono  varchar(150), 
  `key`  varchar(150) NOT NULL, 
  color  varchar(20) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE pagina (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  titulo        varchar(150) NOT NULL, 
  icono         varchar(150) NULL, 
  activo        tinyint(1) DEFAULT 1 NOT NULL, 
  `key`         varchar(150) NOT NULL, 
  tipo_paginaid int(11) NOT NULL, 
  moduloid      int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_pagina (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE usuario (
  id           int(11) NOT NULL AUTO_INCREMENT, 
  correo       varchar(255) NOT NULL UNIQUE, 
  contrasenia  varchar(255) NOT NULL, 
  tipo_usuario char(1) NOT NULL, 
  activo       tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_cliente (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE empresa (
  id                  int(11) NOT NULL AUTO_INCREMENT, 
  nombre              varchar(200) NOT NULL, 
  correo              varchar(200) NOT NULL, 
  nro_telefono        varchar(20) NOT NULL, 
  logo                mediumblob NOT NULL, 
  color_pri           varchar(20) NOT NULL, 
  color_sec           varchar(20) NOT NULL, 
  color_ter           varchar(20) NOT NULL, 
  porcentaje_garantia numeric(9, 2) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE acceso (
  paginaid int(11) NOT NULL, 
  rolid    int(11) NOT NULL, 
  permiso  tinyint(1) NOT NULL, 
  search   tinyint(1) NOT NULL, 
  consult  tinyint(1) NOT NULL, 
  `insert` tinyint(1) NOT NULL, 
  `update` tinyint(1) NOT NULL, 
  `delete` tinyint(1) NOT NULL, 
  unactive tinyint(1) NOT NULL, 
  PRIMARY KEY (paginaid, 
  rolid));
CREATE TABLE tipo_empaque (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(100) NOT NULL, 
  peso_maximo   int(11) NOT NULL, 
  unidad_medida varchar(10), 
  activo        tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_reclamo (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(150) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE motivo_reclamo (
  id             int(11) NOT NULL AUTO_INCREMENT, 
  nombre         varchar(150) NOT NULL, 
  descripcion    text, 
  tipo_reclamoid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE causa_reclamo (
  id               int(11) NOT NULL AUTO_INCREMENT, 
  nombre           varchar(150) NOT NULL, 
  descripcion      text, 
  motivo_reclamoid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE sucursal (
  id            int(10) NOT NULL AUTO_INCREMENT, 
  abreviatura   char(5) NOT NULL UNIQUE, 
  codigo_postal char(5), 
  direccion     varchar(150) NOT NULL, 
  horario_l_v   varchar(255), 
  horario_s_d   varchar(255), 
  latitud       numeric(9, 6), 
  longitud      numeric(9, 6), 
  teléfono      char(255), 
  referencia    varchar(255), 
  activo        tinyint(1) DEFAULT 1 NOT NULL, 
  ubigeocodigo  varchar(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE DESCUENTO (
  id           int(4) NOT NULL AUTO_INCREMENT, 
  nombre       varchar(100) NOT NULL, 
  descripcion  text, 
  fecha_inicio date NOT NULL, 
  fecha_fin    date NOT NULL, 
  activo       tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE DESCUENTO_articulo (
  DESCUENTOid int(4) NOT NULL, 
  articuloid  int(10) NOT NULL, 
  PRIMARY KEY (DESCUENTOid, 
  articuloid));
CREATE TABLE paquete_DESCUENTO (
  paquetetracking int(11) NOT NULL, 
  DESCUENTOid     int(4) NOT NULL, 
  PRIMARY KEY (paquetetracking, 
  DESCUENTOid));
CREATE TABLE estado_encomienda (
  id          int(4) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(200) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
ALTER TABLE sucursal ADD CONSTRAINT FKsucursal756715 FOREIGN KEY (ubigeocodigo) REFERENCES ubigeo (codigo);
ALTER TABLE escala ADD CONSTRAINT FKescala667165 FOREIGN KEY (sucursalid) REFERENCES sucursal (id);
ALTER TABLE escala ADD CONSTRAINT FKescala650496 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s308635 FOREIGN KEY (empleadousuarioid) REFERENCES empleado (usuarioid);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s707218 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE salida ADD CONSTRAINT FKsalida314397 FOREIGN KEY (unidadid) REFERENCES unidad (id);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient915034 FOREIGN KEY (estado_encomiendaid) REFERENCES detalle_estado (id);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve532256 FOREIGN KEY (articuloid) REFERENCES articulo (id);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve813706 FOREIGN KEY (ventanum_serie, ventatipo_comprobanteid) REFERENCES transaccion_venta (num_serie, tipo_comprobanteid);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo902505 FOREIGN KEY (estado_reclamoid) REFERENCES estado_reclamo (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo501927 FOREIGN KEY (tipo_indemnizacionid) REFERENCES tipo_indemnizacion (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo121578 FOREIGN KEY (marcaid) REFERENCES marca (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo83299 FOREIGN KEY (tipo_unidadid) REFERENCES tipo_unidad (id);
ALTER TABLE unidad ADD CONSTRAINT FKunidad608127 FOREIGN KEY (modeloid) REFERENCES modelo (id);
ALTER TABLE metodo_pago_venta ADD CONSTRAINT FKmetodo_pag702897 FOREIGN KEY (metodo_pagoid) REFERENCES metodo_pago (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete148321 FOREIGN KEY (transaccion_encomienda_num_serie) REFERENCES transaccion_encomienda (num_serie);
ALTER TABLE empleado ADD CONSTRAINT FKempleado961716 FOREIGN KEY (rolid) REFERENCES rol (id);
ALTER TABLE articulo ADD CONSTRAINT FKarticulo307124 FOREIGN KEY (tamaño_cajaid) REFERENCES tamanio_caja (id);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient381900 FOREIGN KEY (paquetetracking) REFERENCES paquete (tracking);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete532667 FOREIGN KEY (tipo_recepcionid) REFERENCES tipo_recepcion (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete691155 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete992725 FOREIGN KEY (tipo_documento_destinatario_id) REFERENCES tipo_documento (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut972797 FOREIGN KEY (sucursal_origen_id) REFERENCES sucursal (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut28234 FOREIGN KEY (sucursal_destino_id) REFERENCES sucursal (id);
ALTER TABLE rol ADD CONSTRAINT FKrol677440 FOREIGN KEY (tipo_rolid) REFERENCES tipo_rol (id);
ALTER TABLE cliente ADD CONSTRAINT FKcliente66106 FOREIGN KEY (tipo_documentoid) REFERENCES tipo_documento (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete329420 FOREIGN KEY (contenido_paqueteid) REFERENCES contenido_paquete (id);
ALTER TABLE pagina ADD CONSTRAINT FKpagina910561 FOREIGN KEY (tipo_paginaid) REFERENCES tipo_pagina (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo680466 FOREIGN KEY (paquetetracking) REFERENCES paquete (tracking);
ALTER TABLE transaccion_encomienda ADD CONSTRAINT FKtransaccio662746 FOREIGN KEY (tipo_comprobanteid) REFERENCES tipo_comprobante (id);
ALTER TABLE transaccion_venta ADD CONSTRAINT FKtransaccio293973 FOREIGN KEY (tipo_comprobanteid) REFERENCES tipo_comprobante (id);
ALTER TABLE cliente ADD CONSTRAINT FKcliente404372 FOREIGN KEY (tipo_clienteid) REFERENCES tipo_cliente (id);
ALTER TABLE transaccion_encomienda ADD CONSTRAINT FKtransaccio902557 FOREIGN KEY (clienteid) REFERENCES cliente (usuarioid);
ALTER TABLE transaccion_venta ADD CONSTRAINT FKtransaccio533784 FOREIGN KEY (clienteid) REFERENCES cliente (usuarioid);
ALTER TABLE pagina ADD CONSTRAINT FKpagina193794 FOREIGN KEY (moduloid) REFERENCES modulo (id);
ALTER TABLE acceso ADD CONSTRAINT FKacceso288305 FOREIGN KEY (paginaid) REFERENCES pagina (id);
ALTER TABLE acceso ADD CONSTRAINT FKacceso650542 FOREIGN KEY (rolid) REFERENCES rol (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete94264 FOREIGN KEY (tipo_empaqueid) REFERENCES tipo_empaque (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo555298 FOREIGN KEY (ubigeocodigo) REFERENCES ubigeo (codigo);
ALTER TABLE motivo_reclamo ADD CONSTRAINT FKmotivo_rec334818 FOREIGN KEY (tipo_reclamoid) REFERENCES tipo_reclamo (id);
ALTER TABLE causa_reclamo ADD CONSTRAINT FKcausa_recl554759 FOREIGN KEY (motivo_reclamoid) REFERENCES motivo_reclamo (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo820690 FOREIGN KEY (causa_reclamoid) REFERENCES causa_reclamo (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo970308 FOREIGN KEY (tipo_documentoid) REFERENCES tipo_documento (id);
ALTER TABLE DESCUENTO_articulo ADD CONSTRAINT FKDESCUENTO_871737 FOREIGN KEY (DESCUENTOid) REFERENCES DESCUENTO (id);
ALTER TABLE DESCUENTO_articulo ADD CONSTRAINT FKDESCUENTO_10309 FOREIGN KEY (articuloid) REFERENCES articulo (id);
ALTER TABLE paquete_DESCUENTO ADD CONSTRAINT FKpaquete_DE769291 FOREIGN KEY (paquetetracking) REFERENCES paquete (tracking);
ALTER TABLE paquete_DESCUENTO ADD CONSTRAINT FKpaquete_DE774817 FOREIGN KEY (DESCUENTOid) REFERENCES DESCUENTO (id);
ALTER TABLE detalle_estado ADD CONSTRAINT FKdetalle_es814073 FOREIGN KEY (estado_encomiendaid) REFERENCES estado_encomienda (id);
