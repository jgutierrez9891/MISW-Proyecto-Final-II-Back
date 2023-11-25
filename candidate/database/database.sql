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
    pais varchar(100) NOT NULL,
    ciudad varchar(50) NOT NULL,
    aspiracion_salarial bigint NOT NULL,
    fecha_nacimiento datetime NOT NULL,
    idiomas varchar(200) NOT NULL,
    fecha_ultima_evaluacion datetime DEFAULT NULL,
    promedio_evaluaciones float DEFAULT NULL,
    estado varchar(50) DEFAULT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE entrevista(
    id int not null AUTO_INCREMENT,
    id_candidato int NOT NULL,
    fecha varchar(50) NOT NULL,
    estado varchar(100) NOT NULL,
    nombre_entrevista varchar(100) NULL,
    resultado int NULL,
    id_empresa int NOT NULL,
    PRIMARY KEY(id)
);

insert into candidatos.entrevista (id_candidato, fecha, estado, nombre_entrevista, resultado, id_empresa) values (1,"2023-09-05","finalizado", "inglés", 85, 1);

CREATE TABLE info_tecnica (
  id int NOT NULL AUTO_INCREMENT,
  tipo varchar(50) DEFAULT NULL,
  valor varchar(50) DEFAULT NULL,
  id_candidato int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY id_candidato (id_candidato),
  CONSTRAINT info_tecnica_ibfk_1 FOREIGN KEY (id_candidato) REFERENCES candidato (id)
);

CREATE TABLE info_academica (
  id int NOT NULL AUTO_INCREMENT,
  institucion varchar(50) DEFAULT NULL,
  titulo varchar(50) DEFAULT NULL,
  fecha_inicio varchar(50) DEFAULT NULL,
  fecha_fin varchar(50) DEFAULT NULL,
  id_candidato int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY id_candidato (id_candidato),
  CONSTRAINT info_academica_ibfk_1 FOREIGN KEY (id_candidato) REFERENCES candidato (id)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;

CREATE TABLE info_laboral (
  id int NOT NULL AUTO_INCREMENT,
  cargo varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  ano_inicio int NOT NULL,
  ano_fin int NOT NULL,
  empresa varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion varchar(4000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  id_candidato int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY info_laboral_candidato_idx (id_candidato),
  CONSTRAINT info_laboral_candidato FOREIGN KEY (id_candidato) REFERENCES candidato (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE resultado_prueba_tecnica (
  id int NOT NULL AUTO_INCREMENT,
  candidato_id int NOT NULL,
  nombre varchar(100) NOT NULL,
  fecha_prueba date DEFAULT NULL,
  puntaje int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY candidato_id (candidato_id),
  CONSTRAINT candidato_id_ibfk_1 FOREIGN KEY (candidato_id) REFERENCES candidato (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3;


INSERT INTO candidatos.candidato 
(id, tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas, estado) 
VALUES 
(1001, 'cc', '123456789', 'John Doe', 'john_doe', 'password', '1234567890', 'john.doe@example.com', 'USA', 'New York', 50000, '1990-01-15', 'English, Spanish', 'DISPONIBLE');
INSERT INTO candidatos.candidato 
(id, tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas, estado) 
VALUES 
(1002, 'cc', 'abc123456', 'John Doe', 'john_doe', 'password', '1234567890', 'john.doe@example.com', 'USA', 'New York', 50000, '1990-01-15', 'English, Spanish', 'DISPONIBLE');

INSERT INTO candidatos.resultado_prueba_tecnica 
(id, candidato_id, nombre, fecha_prueba, puntaje) 
VALUES 
(1001, 1001, 'Prueba A', '2023-01-01', 80);



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