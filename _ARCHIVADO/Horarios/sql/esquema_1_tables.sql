create table horario (
  id       int(10) not null auto_increment, 
  dia      int(10) not null, 
  h_inicio int(10) not null, 
  h_final  int(10) not null, 
  grupoid  int(11) not null, 
  primary key (id));
create table curso (
  id          int(11) not null auto_increment, 
  abreviacion varchar(6) not null, 
  nombre      varchar(255) not null, 
  creditos    int(11) not null, 
  ciclo       int(11) not null, 
  colorid     int(11) not null, 
  primary key (id));
create table docente (
  id        int(11) not null auto_increment, 
  nombres   varchar(150) not null, 
  apellidos varchar(150) not null, 
  primary key (id));
create table grupo (
  id             int(11) not null auto_increment, 
  denominacion   char(1) not null, 
  semestrecodigo char(6) not null, 
  cursoid        int(11) not null, 
  docenteid      int(11) not null, 
  primary key (id));
create table semestre (
  codigo   char(6) not null, 
  f_inicio date not null, 
  f_final  date not null, 
  primary key (codigo));
create table color (
  id          int(11) not null auto_increment, 
  nombre      varchar(15) not null, 
  color_fondo varchar(15) not null, 
  color_texto varchar(15) not null, 
  primary key (id));
create table curso_curso (
  cursoid     int(11) not null, 
  cursoid_pre int(11) not null, 
  primary key (cursoid, 
  cursoid_pre));
create table alumno (
  id          int(11) not null auto_increment, 
  nombres     varchar(150) not null, 
  apellidos   varchar(150) not null, 
  codigo      varchar(20) not null, 
  contrasenia varchar(150) not null, 
  primary key (id));
create table matricula (
  id             int(11) not null auto_increment, 
  alumnoid       int(11) not null, 
  semestrecodigo char(6) not null, 
  primary key (id));
create table detalles_matricula (
  grupoid     int(11) not null, 
  matriculaid int(11) not null, 
  primary key (grupoid, 
  matriculaid));
create table modelo (
  id             int(11) not null auto_increment, 
  nombre         varchar(55) not null, 
  alumnoid       int(11) not null, 
  semestrecodigo char(6) not null, 
  primary key (id));
create table grupo_modelo (
  grupoid  int(11) not null, 
  modeloid int(11) not null, 
  primary key (grupoid, 
  modeloid));
alter table grupo add constraint FKgrupo65739 foreign key (semestrecodigo) references semestre (codigo);
alter table grupo add constraint FKgrupo646143 foreign key (cursoid) references curso (id);
alter table grupo add constraint FKgrupo55510 foreign key (docenteid) references docente (id);
alter table horario add constraint FKhorario682240 foreign key (grupoid) references grupo (id);
alter table curso add constraint FKcurso421515 foreign key (colorid) references color (id);
alter table curso_curso add constraint FKcurso_curs955408 foreign key (cursoid) references curso (id);
alter table curso_curso add constraint FKcurso_curs627155 foreign key (cursoid_pre) references curso (id);
alter table detalles_matricula add constraint FKdetalles_m96921 foreign key (grupoid) references grupo (id);
alter table detalles_matricula add constraint FKdetalles_m3019 foreign key (matriculaid) references matricula (id);
alter table matricula add constraint FKmatricula928478 foreign key (alumnoid) references alumno (id);
alter table matricula add constraint FKmatricula699956 foreign key (semestrecodigo) references semestre (codigo);
alter table modelo add constraint FKmodelo712826 foreign key (alumnoid) references alumno (id);
alter table grupo_modelo add constraint FKgrupo_mode463927 foreign key (grupoid) references grupo (id);
alter table grupo_modelo add constraint FKgrupo_mode815667 foreign key (modeloid) references modelo (id);
alter table modelo add constraint FKmodelo630328 foreign key (semestrecodigo) references semestre (codigo);
