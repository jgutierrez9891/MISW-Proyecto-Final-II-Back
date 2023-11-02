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