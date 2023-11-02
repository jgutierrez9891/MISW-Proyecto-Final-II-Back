CREATE DATABASE empresas;
use empresas;

ALTER DATABASE empresas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE empresa(
    id int not null AUTO_INCREMENT,
    tipo_doc varchar(10) NOT NULL,
    num_doc varchar(50) NOT NULL,
    nombre varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    telefono varchar(30) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE representante(
    id int not null AUTO_INCREMENT,
    tipo_doc varchar(10) NOT NULL,
    num_doc varchar(50) NOT NULL,
    nombre varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    telefono varchar(30) NOT NULL,
    usuario varchar(50) NOT NULL,
    clave varchar(50) NOT NULL,
    id_empresa int NOT NULL,
    PRIMARY KEY(id)
);



CREATE TABLE proyecto(
    id int not null AUTO_INCREMENT,
    titulo varchar(100) NOT NULL,
    fecha_inicio datetime,
    fecha_fin datetime,
    id_empresa int not null,
    PRIMARY KEY(id)
);

CREATE TABLE ficha_trabajo(
    id int not null AUTO_INCREMENT,
    nombre varchar(100) NOT NULL,
    descripcion varchar(2000),
    id_empresa int not null,
    id_proyecto int,
    PRIMARY KEY(id)
);


CREATE TABLE rol(
    id_rol int not null AUTO_INCREMENT,
    nombre varchar(60) NOT NULL,
    descripcion varchar(250),
    id_equipo int,
    PRIMARY KEY(id_rol)
);

CREATE TABLE habilidad(
    id_habilidad int not null AUTO_INCREMENT,
    habilidad varchar(60) NOT NULL,
    tipo varchar(60),
    PRIMARY KEY(id_habilidad)
);

CREATE TABLE rol_habilidad(
    id_asoc int not null AUTO_INCREMENT,
    id_rol int  not null,
    id_habilidad int not null,
    PRIMARY KEY(id_asoc)
);

insert into empresas.rol (nombre, descripcion, id_equipo) value ("empresa prueba", "descripcion prueba", 1)
insert into empresas.habilidad (habilidad, tipo) value ("habilidad prueba 1", "blanda")
insert into empresas.habilidad (habilidad, tipo) value ("habilidad prueba 2", "tecnica")
insert into empresas.habilidad (habilidad, tipo) value ("habilidad prueba 3", "blanda")
insert into empresas.rol_habilidad (id_rol, id_habilidad) value (1,1)
insert into empresas.rol_habilidad (id_rol, id_habilidad) value (1,2)