CREATE DATABASE candidatos;
use candidatos;

ALTER DATABASE candidatos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE candidato(
    id int not null AUTO_INCREMENT,
    tipo_doc varchar(10) NOT NULL,
    num_doc varchar(50) NOT NULL,
    nombre varchar(100) NOT NULL,
    usuario varchar(50) NOT NULL,
    clave varchar(50) NOT NULL,
    telefono varchar(30) NOT NULL,
    email varchar(100) NOT NULL,
    pais varchar(50) NOT NULL,
    ciudad varchar(50) NOT NULL,
    aspiracion_salarial bigint NOT NULL,
    fecha_nacimiento datetime NOT NULL,
    idiomas varchar(200) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO candidatos.candidato (tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas) VALUES ("CC", "10154377744","daniel chala", "daachalabu", "123", "3002291914","edelcozgran@hotmail.com","Colombia","Bogotá",5000000,"1989-03-02","Ingles");

CREATE DATABASE empresas;
use empresas;

ALTER DATABASE empresas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE empresa(
    id int not null AUTO_INCREMENT,
    tipo_doc varchar(10) NOT NULL,
    num_doc varchar(50) NOT NULL,
    email varchar(100) NOT NULL,
    telefono varchar(30) NOT NULL,
    nombre varchar(50) NOT NULL,
    PRIMARY KEY(id)
);

insert into empresas.empresa (tipo_doc, num_doc, email, telefono, nombre) values ("NITs","1010999-10","daachalabu@unal.edu.co", 300229,"empresa Prueba");


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

insert into empresas.representante (tipo_doc, num_doc, nombre, email, telefono, usuario, clave, id_empresa) values ("CC","1023456789","Mauricio Peña", "daachalabu@unal.edu.co", 3123456789,"maupena", "miclave123", 1);
