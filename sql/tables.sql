CREATE TABLE articulo (
  id            int(10) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(100) NOT NULL, 
  precio        numeric(9, 2) NOT NULL, 
  stock         int(11) NOT NULL, 
  activo        tinyint(1) NOT NULL, 
  img           text NOT NULL, 
  dimensiones   varchar(20), 
  tamaño_cajaid int(11), 
  PRIMARY KEY (id));
CREATE TABLE causa_reclamo (
  id               int(11) NOT NULL AUTO_INCREMENT, 
  nombre           varchar(150) NOT NULL, 
  descripcion      text, 
  motivo_reclamoid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE cliente (
  id               int(10) NOT NULL AUTO_INCREMENT, 
  correo           varchar(250) NOT NULL, 
  telefono         varchar(15), 
  num_documento    varchar(20) NOT NULL, 
  nombre_siglas    varchar(150) NOT NULL, 
  apellidos_razon  varchar(150) NOT NULL, 
  tipo_documentoid int(11) NOT NULL, 
  tipo_clienteid   int(11) NOT NULL, 
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
CREATE TABLE descuento (
  id           int(4) NOT NULL AUTO_INCREMENT, 
  nombre       varchar(100) NOT NULL, 
  descripcion  text, 
  fecha_inicio date NOT NULL, 
  fecha_fin    date NOT NULL, 
  activo       tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE descuento_articulo (
  descuentoid        int(4) NOT NULL, 
  articuloid         int(10) NOT NULL, 
  cantidad_descuento numeric(9, 2) NOT NULL, 
  PRIMARY KEY (descuentoid, 
  articuloid));
CREATE TABLE detalle_estado (
  id                  int(10) NOT NULL AUTO_INCREMENT, 
  nombre              varchar(50) NOT NULL, 
  descripcion         text, 
  activo              tinyint(1) DEFAULT 1 NOT NULL, 
  estado_encomiendaid int(4) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE detalle_reclamo (
  id               int(10) NOT NULL AUTO_INCREMENT, 
  nombre           varchar(50) NOT NULL, 
  descripcion      text, 
  activo           tinyint(1) DEFAULT 1 NOT NULL, 
  estado_reclamoid int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE detalle_venta (
  articuloid     int(10) NOT NULL, 
  ventanum_serie int(11) NOT NULL, 
  cantidad       int(10) NOT NULL, 
  PRIMARY KEY (articuloid, 
  ventanum_serie));
CREATE TABLE empleado (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(150) NOT NULL, 
  apellidos   varchar(150) NOT NULL, 
  correo      varchar(250) NOT NULL UNIQUE, 
  n_documento varchar(11) NOT NULL, 
  rolid       int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE empleado_salida (
  salidaid   int(10) NOT NULL, 
  empleadoid int(10) NOT NULL, 
  PRIMARY KEY (salidaid, 
  empleadoid));
CREATE TABLE empresa (
  id                int(11) NOT NULL AUTO_INCREMENT, 
  nombre            varchar(200) NOT NULL, 
  correo            varchar(250) NOT NULL, 
  nro_telefono      varchar(20) NOT NULL, 
  logo              text NOT NULL, 
  color_pri         varchar(20) NOT NULL, 
  color_sec         varchar(20) NOT NULL, 
  color_ter         varchar(20) NOT NULL, 
  porcentaje_recojo numeric(9, 2) NOT NULL, 
  ruc               char(11) NOT NULL, 
  id_sucursal       int(11) NOT NULL, 
  igv               numeric(9, 2) NOT NULL, 
  actual            tinyint(1) DEFAULT 1 NOT NULL, 
  fecha             date DEFAULT CURRENT_DATE NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE escala (
  sucursalid int(10) NOT NULL, 
  salidaid   int(10) NOT NULL, 
  PRIMARY KEY (sucursalid, 
  salidaid));
CREATE TABLE estado_encomienda (
  id          int(4) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(200) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  tipoEstado  char(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE estado_reclamo (
  id     int(10) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE marca (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(20) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE mensaje_contacto (
  id               int(4) NOT NULL AUTO_INCREMENT, 
  nombre           varchar(200) NOT NULL, 
  nro_documento    varchar(20) NOT NULL, 
  correo           varchar(250) NOT NULL, 
  telefono         varchar(15) NOT NULL, 
  mensaje          text NOT NULL, 
  tipo_documentoid int(11) NOT NULL, 
  tipo_clienteid   int(11) NOT NULL, 
  sucursalid       int(10) NOT NULL, 
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
CREATE TABLE modalidad_pago (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(200) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE modelo (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(20) NOT NULL, 
  activo        tinyint(1) NOT NULL, 
  marcaid       int(11) NOT NULL, 
  tipo_unidadid int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE modulo (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(150) NOT NULL, 
  icono  varchar(150), 
  `key`  varchar(150) NOT NULL, 
  color  varchar(20) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  img    text, 
  PRIMARY KEY (id));
CREATE TABLE motivo_reclamo (
  id             int(11) NOT NULL AUTO_INCREMENT, 
  nombre         varchar(150) NOT NULL, 
  descripcion    text, 
  tipo_reclamoid int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE pagina (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  titulo        varchar(150) NOT NULL, 
  icono         varchar(150), 
  activo        tinyint(1) DEFAULT 1 NOT NULL, 
  `key`         varchar(150) NOT NULL, 
  mostrar       tinyint(1) DEFAULT 1, 
  padrepaginaid int(11), 
  tipo_paginaid int(11) NOT NULL, 
  moduloid      int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE paquete (
  tracking                         int(11) NOT NULL AUTO_INCREMENT, 
  clave                            char(4) NOT NULL, 
  valor                            numeric(9, 2) NOT NULL, 
  peso                             numeric(9, 2) NOT NULL, 
  qr_url                           text, 
  alto                             numeric(9, 2), 
  cantidad_folios                  int(11), 
  estado_pago                      char(1) NOT NULL, 
  largo                            numeric(9, 2), 
  precio_ruta                      numeric(9, 2) NOT NULL, 
  ancho                            numeric(9, 2), 
  descripcion                      text, 
  nombres_contacto_destinatario    varchar(255) NOT NULL, 
  apellidos_razon_destinatario     varchar(255) NOT NULL, 
  direccion_destinatario           varchar(255), 
  telefono_destinatario            varchar(20) NOT NULL, 
  num_documento_destinatario       varchar(25) NOT NULL, 
  sucursal_destino_id              int(11) NOT NULL, 
  tipo_documento_destinatario_id   int(11) NOT NULL, 
  tipo_empaqueid                   int(11) NOT NULL, 
  contenido_paqueteid              int(11), 
  tipo_recepcionid                 int(11) NOT NULL, 
  salidaid                         int(10), 
  transaccion_encomienda_num_serie int(11), 
  modalidad_pagoid                 int(11) NOT NULL, 
  PRIMARY KEY (tracking));
CREATE TABLE paquete_descuento (
  paquetetracking int(11) NOT NULL, 
  descuentoid     int(4) NOT NULL, 
  cantidad        numeric(9, 2) NOT NULL, 
  PRIMARY KEY (paquetetracking, 
  descuentoid));
CREATE TABLE permiso (
  paginaid int(11) NOT NULL, 
  rolid    int(11) NOT NULL, 
  acceso   tinyint(1) NOT NULL, 
  search   tinyint(1) NOT NULL, 
  consult  tinyint(1) NOT NULL, 
  `insert` tinyint(1) NOT NULL, 
  `update` tinyint(1) NOT NULL, 
  `delete` tinyint(1) NOT NULL, 
  unactive tinyint(1) NOT NULL, 
  otro     text DEFAULT '{}', 
  PRIMARY KEY (paginaid, 
  rolid));
CREATE TABLE pregunta_frecuente (
  id          int(4) NOT NULL AUTO_INCREMENT, 
  titulo      text NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE reclamo (
  id                   int(10) NOT NULL AUTO_INCREMENT, 
  nombres_razon        varchar(200) NOT NULL, 
  direccion            text NOT NULL, 
  correo               varchar(250) NOT NULL, 
  telefono             char(9) NOT NULL, 
  n_documento          varchar(11) NOT NULL, 
  monto_indemnizado    numeric(9, 2), 
  bien_contratado      char(1) NOT NULL comment 'Producto (P)
Servicio (S)
 ', 
  monto_reclamado      numeric(9, 2) NOT NULL, 
  relacion             char(1) comment 'Quien envía
Quien recibe
 ', 
  fecha_recepcion      date NOT NULL, 
  sucursal_id          int(11) NOT NULL, 
  descripcion          text NOT NULL, 
  detalles             text, 
  pedido               text, 
  foto                 text, 
  causa_reclamoid      int(11) NOT NULL, 
  tipo_indemnizacionid int(10), 
  paquetetracking      int(11) NOT NULL, 
  ubigeocodigo         varchar(10), 
  tipo_documentoid     int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE regla_cargo (
  id             int(4) NOT NULL AUTO_INCREMENT, 
  tipo_condicion char(1) NOT NULL, 
  inferior       numeric(9, 2) NOT NULL, 
  superior       numeric(9, 2), 
  porcentaje     numeric(9, 2) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE rol (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(250) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  tipo_rolid  int(10) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE salida (
  id                  int(10) NOT NULL AUTO_INCREMENT, 
  fecha               date NOT NULL, 
  hora                time NOT NULL, 
  recojo              tinyint(1) NOT NULL, 
  entrega             tinyint(1) NOT NULL, 
  estado              char(1) NOT NULL, 
  unidadid            int(10) NOT NULL, 
  destino_final_id    int(10) NOT NULL, 
  conductor_principal int(11) NOT NULL, 
  origen_inicio_id    int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE seguimiento (
  paquetetracking    int(11) NOT NULL, 
  detalle_estadoid   int(10) NOT NULL, 
  fecha              date NOT NULL, 
  hora               time NOT NULL, 
  tipo_comprobanteid int(10), 
  PRIMARY KEY (paquetetracking, 
  detalle_estadoid));
CREATE TABLE seguimiento_reclamo (
  reclamoid         int(10) NOT NULL, 
  detalle_reclamoid int(10) NOT NULL, 
  fecha             date NOT NULL, 
  hora              time NOT NULL, 
  PRIMARY KEY (reclamoid, 
  detalle_reclamoid));
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
CREATE TABLE tamanio_caja (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(3) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tarifa_ruta (
  sucursal_origen_id  int(10) NOT NULL, 
  sucursal_destino_id int(10) NOT NULL, 
  tarifa              numeric(9, 2) NOT NULL, 
  PRIMARY KEY (sucursal_origen_id, 
  sucursal_destino_id));
CREATE TABLE tipo_cliente (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_comprobante (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  inicial     varchar(3) NOT NULL, 
  nombre      varchar(50) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  tipo_uso    char(1), 
  PRIMARY KEY (id));
CREATE TABLE tipo_documento (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  siglas char(3) NOT NULL, 
  nombre varchar(100) NOT NULL, 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_empaque (
  id            int(11) NOT NULL AUTO_INCREMENT, 
  nombre        varchar(100) NOT NULL, 
  peso_maximo   int(11) NOT NULL, 
  unidad_medida varchar(10), 
  activo        tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_indemnizacion (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(150) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_pagina (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_recepcion (
  id     int(11) NOT NULL AUTO_INCREMENT, 
  nombre varchar(100) NOT NULL comment 'Recojo en tienda
Envío a domicilio
Con recojo y pago en tienda
 ', 
  activo tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_reclamo (
  id          int(11) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(150) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_rol (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(250) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE tipo_unidad (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(20) NOT NULL, 
  descripcion text, 
  activo      tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE transaccion_encomienda (
  num_serie          int(11) NOT NULL AUTO_INCREMENT, 
  masivo             tinyint(1) NOT NULL comment ' 1 si es envío masivo
0 si es un empaque (paquete o sobre)
 ', 
  descripcion        text, 
  monto_total        numeric(9, 2), 
  recojo_casa        tinyint(1), 
  id_sucursal_origen int(11) NOT NULL, 
  fecha              date NOT NULL, 
  hora               time NOT NULL, 
  direccion_recojo   varchar(255), 
  clienteid          int(10) NOT NULL, 
  PRIMARY KEY (num_serie));
CREATE TABLE transaccion_venta (
  num_serie          int(11) NOT NULL AUTO_INCREMENT, 
  tipo_comprobanteid int(10) NOT NULL, 
  estado             tinyint(1) DEFAULT 0 NOT NULL, 
  monto_total        numeric(9, 2), 
  fecha              date NOT NULL, 
  hora               time NOT NULL, 
  clienteid          int(10) NOT NULL, 
  PRIMARY KEY (num_serie));
CREATE TABLE ubigeo (
  codigo       varchar(10) NOT NULL, 
  departamento varchar(150) NOT NULL, 
  provincia    varchar(150) NOT NULL, 
  distrito     varchar(150) NOT NULL, 
  activo       tinyint(1) DEFAULT 1 NOT NULL, 
  PRIMARY KEY (codigo));
CREATE TABLE unidad (
  id           int(10) NOT NULL AUTO_INCREMENT, 
  placa        varchar(8) NOT NULL UNIQUE, 
  MTC          char(9) NOT NULL UNIQUE, 
  TUC          char(12) NOT NULL UNIQUE, 
  capacidad    numeric(9, 2) NOT NULL, 
  volumen      numeric(9, 2) NOT NULL, 
  descripcion  text, 
  estado       char(1) NOT NULL, 
  fecha_compra date, 
  modeloid     int(11) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE usuario (
  id           int(11) NOT NULL AUTO_INCREMENT, 
  correo       varchar(250) NOT NULL UNIQUE, 
  contrasenia  varchar(255) NOT NULL, 
  tipo_usuario char(1) NOT NULL, 
  activo       tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient92123 FOREIGN KEY (tipo_comprobanteid) REFERENCES tipo_comprobante (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete940812 FOREIGN KEY (modalidad_pagoid) REFERENCES modalidad_pago (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete94264 FOREIGN KEY (tipo_empaqueid) REFERENCES tipo_empaque (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete329420 FOREIGN KEY (contenido_paqueteid) REFERENCES contenido_paquete (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete992725 FOREIGN KEY (tipo_documento_destinatario_id) REFERENCES tipo_documento (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete691155 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete532667 FOREIGN KEY (tipo_recepcionid) REFERENCES tipo_recepcion (id);
ALTER TABLE paquete ADD CONSTRAINT FKpaquete148321 FOREIGN KEY (transaccion_encomienda_num_serie) REFERENCES transaccion_encomienda (num_serie);
ALTER TABLE paquete_descuento ADD CONSTRAINT FKpaquete_de604728 FOREIGN KEY (paquetetracking) REFERENCES paquete (tracking);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo680466 FOREIGN KEY (paquetetracking) REFERENCES paquete (tracking);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient381900 FOREIGN KEY (paquetetracking) REFERENCES paquete (tracking);
ALTER TABLE seguimiento ADD CONSTRAINT FKseguimient567863 FOREIGN KEY (detalle_estadoid) REFERENCES detalle_estado (id);
ALTER TABLE seguimiento_reclamo ADD CONSTRAINT FKseguimient644896 FOREIGN KEY (detalle_reclamoid) REFERENCES detalle_reclamo (id);
ALTER TABLE seguimiento_reclamo ADD CONSTRAINT FKseguimient693109 FOREIGN KEY (reclamoid) REFERENCES reclamo (id);
ALTER TABLE detalle_reclamo ADD CONSTRAINT FKdetalle_re335454 FOREIGN KEY (estado_reclamoid) REFERENCES estado_reclamo (id);
ALTER TABLE mensaje_contacto ADD CONSTRAINT FKmensaje_co839897 FOREIGN KEY (sucursalid) REFERENCES sucursal (id);
ALTER TABLE mensaje_contacto ADD CONSTRAINT FKmensaje_co632658 FOREIGN KEY (tipo_clienteid) REFERENCES tipo_cliente (id);
ALTER TABLE mensaje_contacto ADD CONSTRAINT FKmensaje_co868453 FOREIGN KEY (tipo_documentoid) REFERENCES tipo_documento (id);
ALTER TABLE detalle_estado ADD CONSTRAINT FKdetalle_es814073 FOREIGN KEY (estado_encomiendaid) REFERENCES estado_encomienda (id);
ALTER TABLE paquete_descuento ADD CONSTRAINT FKpaquete_de412901 FOREIGN KEY (descuentoid) REFERENCES descuento (id);
ALTER TABLE descuento_articulo ADD CONSTRAINT FKdescuento_822045 FOREIGN KEY (articuloid) REFERENCES articulo (id);
ALTER TABLE descuento_articulo ADD CONSTRAINT FKdescuento_629531 FOREIGN KEY (descuentoid) REFERENCES descuento (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo970308 FOREIGN KEY (tipo_documentoid) REFERENCES tipo_documento (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo820690 FOREIGN KEY (causa_reclamoid) REFERENCES causa_reclamo (id);
ALTER TABLE causa_reclamo ADD CONSTRAINT FKcausa_recl554759 FOREIGN KEY (motivo_reclamoid) REFERENCES motivo_reclamo (id);
ALTER TABLE motivo_reclamo ADD CONSTRAINT FKmotivo_rec334818 FOREIGN KEY (tipo_reclamoid) REFERENCES tipo_reclamo (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo555298 FOREIGN KEY (ubigeocodigo) REFERENCES ubigeo (codigo);
ALTER TABLE permiso ADD CONSTRAINT FKpermiso814160 FOREIGN KEY (rolid) REFERENCES rol (id);
ALTER TABLE permiso ADD CONSTRAINT FKpermiso451923 FOREIGN KEY (paginaid) REFERENCES pagina (id);
ALTER TABLE pagina ADD CONSTRAINT FKpagina193794 FOREIGN KEY (moduloid) REFERENCES modulo (id);
ALTER TABLE transaccion_venta ADD CONSTRAINT FKtransaccio322313 FOREIGN KEY (clienteid) REFERENCES cliente (id);
ALTER TABLE transaccion_encomienda ADD CONSTRAINT FKtransaccio308913 FOREIGN KEY (clienteid) REFERENCES cliente (id);
ALTER TABLE cliente ADD CONSTRAINT FKcliente404372 FOREIGN KEY (tipo_clienteid) REFERENCES tipo_cliente (id);
ALTER TABLE transaccion_venta ADD CONSTRAINT FKtransaccio293973 FOREIGN KEY (tipo_comprobanteid) REFERENCES tipo_comprobante (id);
ALTER TABLE pagina ADD CONSTRAINT FKpagina910561 FOREIGN KEY (tipo_paginaid) REFERENCES tipo_pagina (id);
ALTER TABLE cliente ADD CONSTRAINT FKcliente66106 FOREIGN KEY (tipo_documentoid) REFERENCES tipo_documento (id);
ALTER TABLE rol ADD CONSTRAINT FKrol677440 FOREIGN KEY (tipo_rolid) REFERENCES tipo_rol (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut28234 FOREIGN KEY (sucursal_destino_id) REFERENCES sucursal (id);
ALTER TABLE tarifa_ruta ADD CONSTRAINT FKtarifa_rut972797 FOREIGN KEY (sucursal_origen_id) REFERENCES sucursal (id);
ALTER TABLE articulo ADD CONSTRAINT FKarticulo307124 FOREIGN KEY (tamaño_cajaid) REFERENCES tamanio_caja (id);
ALTER TABLE empleado ADD CONSTRAINT FKempleado961716 FOREIGN KEY (rolid) REFERENCES rol (id);
ALTER TABLE metodo_pago_venta ADD CONSTRAINT FKmetodo_pag702897 FOREIGN KEY (metodo_pagoid) REFERENCES metodo_pago (id);
ALTER TABLE unidad ADD CONSTRAINT FKunidad608127 FOREIGN KEY (modeloid) REFERENCES modelo (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo83299 FOREIGN KEY (tipo_unidadid) REFERENCES tipo_unidad (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo121578 FOREIGN KEY (marcaid) REFERENCES marca (id);
ALTER TABLE reclamo ADD CONSTRAINT FKreclamo501927 FOREIGN KEY (tipo_indemnizacionid) REFERENCES tipo_indemnizacion (id);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve86549 FOREIGN KEY (ventanum_serie) REFERENCES transaccion_venta (num_serie);
ALTER TABLE detalle_venta ADD CONSTRAINT FKdetalle_ve532256 FOREIGN KEY (articuloid) REFERENCES articulo (id);
ALTER TABLE salida ADD CONSTRAINT FKsalida314397 FOREIGN KEY (unidadid) REFERENCES unidad (id);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s707218 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE empleado_salida ADD CONSTRAINT FKempleado_s895470 FOREIGN KEY (empleadoid) REFERENCES empleado (id);
ALTER TABLE escala ADD CONSTRAINT FKescala650496 FOREIGN KEY (salidaid) REFERENCES salida (id);
ALTER TABLE escala ADD CONSTRAINT FKescala667165 FOREIGN KEY (sucursalid) REFERENCES sucursal (id);
ALTER TABLE sucursal ADD CONSTRAINT FKsucursal756715 FOREIGN KEY (ubigeocodigo) REFERENCES ubigeo (codigo);
