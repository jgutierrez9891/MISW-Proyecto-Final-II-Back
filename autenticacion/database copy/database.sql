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
    telefono bigint NOT NULL,
    email varchar(100) NOT NULL,
    pais varchar(50) NOT NULL,
    ciudad varchar(50) NOT NULL,
    aspiracion_salarial bigint NOT NULL,
    fecha_nacimiento datetime NOT NULL,
    idiomas varchar(200) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE entrevista(
    id int not null AUTO_INCREMENT,
    id_candidato int NOT NULL,
    fecha varchar(50) NOT NULL,
    estado varchar(100) NOT NULL,
    id_empresa int NOT NULL,
    PRIMARY KEY(id)
);

insert into candidatos.entrevista (id_candidato, fecha, estado, id_empresa) values (1,"2023-09-05","finalizado",1);


CREATE DATABASE empresas;
use empresas;

ALTER DATABASE empresas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE empresa(
    id int not null AUTO_INCREMENT,
    tipo_doc varchar(10) NOT NULL,
    num_doc varchar(50) NOT NULL,
    email varchar(100) NOT NULL,
    telefono varchar(50) NOT NULL,
    nombre varchar(50) NOT NULL,
    PRIMARY KEY(id)
);

insert into empresas.empresa (tipo_doc, num_doc, email, telefono, nombre) values ("NIT","1010999-9","daachalabu@unal.edu.co", 300229,"empresa Prueba");