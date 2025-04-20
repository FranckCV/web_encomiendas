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
CREATE TABLE tipo_unidad (
  id          int(10) NOT NULL AUTO_INCREMENT, 
  nombre      varchar(20) NOT NULL, 
  descripcion text NOT NULL, 
  activo      tinyint(1) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE unidad (
  id            int(10) NOT NULL AUTO_INCREMENT, 
  placa         varchar(10) NOT NULL UNIQUE, 
  capacidad     numeric(9, 2) NOT NULL, 
  volumen       numeric(9, 2) NOT NULL, 
  observaciones text NOT NULL, 
  activo        tinyint(1) NOT NULL, 
  modeloid      int(11) NOT NULL, 
  PRIMARY KEY (id));
ALTER TABLE unidad ADD CONSTRAINT FKunidad608127 FOREIGN KEY (modeloid) REFERENCES modelo (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo121578 FOREIGN KEY (marcaid) REFERENCES marca (id);
ALTER TABLE modelo ADD CONSTRAINT FKmodelo83299 FOREIGN KEY (tipo_unidadid) REFERENCES tipo_unidad (id);
