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

INSERT into empresas.empresa (id, tipo_doc, num_doc, nombre, email, telefono) value (1, "Test", "Test", "Test", "Test", "Test");
INSERT into empresas.empresa (id, tipo_doc, num_doc, nombre, email, telefono) value (101, "Test", "Test", "Test", "Test", "Test");

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

INSERT into empresas.proyecto (id, titulo, id_empresa) value (1, "Test 0", 1);
INSERT into empresas.proyecto (id, titulo, id_empresa) value (2, "Test 0.2", 1);
INSERT into empresas.proyecto (id, titulo, id_empresa) value (7, "Test", 1);
INSERT into empresas.proyecto (id, titulo, id_empresa) value (700, "Test 2", 1);
INSERT into empresas.proyecto (id, titulo, id_empresa) value (770, "Test 3", 1);

CREATE TABLE ficha_trabajo (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  descripcion varchar(2000) DEFAULT NULL,
  id_proyecto int DEFAULT NULL,
  id_empresa int NOT NULL,
  PRIMARY KEY (id),
  KEY fk_ficha_trabajo_proyecto_idx (id_proyecto),
  CONSTRAINT fk_ficha_trabajo_proyecto FOREIGN KEY (id_proyecto) REFERENCES proyecto (id)
);

INSERT into empresas.ficha_trabajo (id, nombre, id_empresa) value (401, "Ficha 4", 101);
INSERT into empresas.ficha_trabajo (id, nombre, id_empresa) value (101, "Ficha 1", 101);

CREATE TABLE hoja_trabajo (
  id int NOT NULL AUTO_INCREMENT,
  nombre_trabajo varchar(100) NOT NULL,
  descripcion_candidato_ideal varchar(5000) DEFAULT NULL,
  id_proyecto int NOT NULL,
  PRIMARY KEY (id),
  KEY fk_hoja_trabajo_proyecto_idx (id_proyecto),
  CONSTRAINT fk_hoja_trabajo_proyecto FOREIGN KEY (id_proyecto) REFERENCES proyecto (id)
);

INSERT into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) value (7010,'Test Job 1', 'Description 1', 700);
INSERT into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) value (7011, 'Test Job 2', 'Description 2', 700);
INSERT into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) value (701, 'Test Job 2', 'Description 2', 770);

CREATE TABLE candidatos_hoja_trabajo (
  id int NOT NULL AUTO_INCREMENT,
  id_hoja_trabajo int NOT NULL,
  id_candidato int NOT NULL,
  PRIMARY KEY (id),
  KEY fk_candidatos_hoja_trabajo_idx (id_hoja_trabajo),
  CONSTRAINT fk_candidatos_hoja_trabajo FOREIGN KEY (id_hoja_trabajo) REFERENCES hoja_trabajo (id)
); 

INSERT into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) value (701,10);
INSERT into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) value (701,20);

CREATE TABLE rol(
    id_rol int not null AUTO_INCREMENT,
    nombre varchar(60) NOT NULL,
    descripcion varchar(250),
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

CREATE TABLE empleado_ficha_trabajo (
  id int NOT NULL AUTO_INCREMENT,
  id_ficha_trabajo int DEFAULT NULL,
  id_empleado int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY id_ficha_trabajo (id_ficha_trabajo),
  CONSTRAINT empleado_ficha_trabajo_ibfk_1 FOREIGN KEY (id_ficha_trabajo) REFERENCES ficha_trabajo (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE empresas.rol_ficha_trabajo (
	id INT AUTO_INCREMENT PRIMARY KEY,
    id_ficha_trabajo INT,
    id_rol INT,
    FOREIGN KEY (id_ficha_trabajo) REFERENCES empresas.ficha_trabajo(id),
    FOREIGN KEY (id_rol) REFERENCES empresas.rol(id_rol)
);

insert into empresas.rol (id_rol, nombre, descripcion) value (5,"prueba 5", "descripcion 4");
insert into empresas.rol (id_rol, nombre, descripcion) value (4,"prueba 4", "descripcion 4");
insert into empresas.rol (id_rol, nombre, descripcion) value (2,"prueba 2", "descripcion 2");
insert into empresas.rol (id_rol, nombre, descripcion) value (1,"prueba 1", "descripcion 1");
-- insert into empresas.proyecto (titulo, fecha_inicio, fecha_fin, id_empresa) value ("proyecto prueba", STR_TO_DATE('2023-01-01', '%Y-%m-%d'), STR_TO_DATE('2023-01-01', '%Y-%m-%d'),1);
-- insert into empresas.ficha_trabajo (nombre, descripcion,id_proyecto, id_empresa) value ("equipo prueba", "descripcion prueba equipo",1,1);
insert into empresas.rol_ficha_trabajo (id_ficha_trabajo, id_rol) value (401, 4);
insert into empresas.rol_ficha_trabajo (id_ficha_trabajo, id_rol) value (401, 5);
insert into empresas.habilidad (habilidad, tipo) value ("habilidad prueba 1", "blanda");
insert into empresas.habilidad (habilidad, tipo) value ("habilidad prueba 2", "tecnica");
insert into empresas.habilidad (habilidad, tipo) value ("habilidad prueba 3", "blanda");
insert into empresas.rol_habilidad (id_rol, id_habilidad) value (1,1);
insert into empresas.rol_habilidad (id_rol, id_habilidad) value (1,2);



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
  tipo varchar(50) DEFAULT NULL,
  valor varchar(50) DEFAULT NULL,
  ano_finalizacion varchar(4) DEFAULT NULL,
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



CREATE DATABASE empleados;
use empleados;

ALTER DATABASE empleados CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE empleado (
  id int NOT NULL AUTO_INCREMENT,
  tipo_doc varchar(50) DEFAULT NULL,
  num_doc varchar(50) DEFAULT NULL,
  nombre varchar(100) DEFAULT NULL,
  usuario varchar(50) DEFAULT NULL,
  telefono varchar(30) DEFAULT NULL,
  email varchar(100) DEFAULT NULL,
  pais varchar(100) DEFAULT NULL,
  ciudad varchar(50) DEFAULT NULL,
  fecha_nacimiento date DEFAULT NULL,
  idiomas varchar(200) DEFAULT NULL,
  estado varchar(50) DEFAULT NULL,
  fecha_evaluacion date DEFAULT NULL,
  evaluaciones int DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3;

insert into empleados.empleado (id, nombre) values (10,"name 1");
insert into empleados.empleado (id, nombre) values (20,"name 2");
insert into empleados.empleado (id, nombre) values (301,"name 2");

CREATE TABLE empleado_evaluacion (
  id int NOT NULL AUTO_INCREMENT,
  evaluacion varchar(1000) DEFAULT NULL,
  puntaje int DEFAULT NULL,
  empleado_id int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY empleado_id (empleado_id),
  CONSTRAINT empleado_evaluacion_ibfk_1 FOREIGN KEY (empleado_id) REFERENCES empleado (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3;

CREATE TABLE habilidadesemp (
  id int NOT NULL AUTO_INCREMENT,
  habilidad varchar(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY habilidad (habilidad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE empleado_habilidad (
  id int NOT NULL AUTO_INCREMENT,
  empleado_id int NOT NULL,
  habilidad_id int NOT NULL,
  PRIMARY KEY (id),
  KEY empleado_id (empleado_id),
  KEY habilidad_id (habilidad_id),
  CONSTRAINT empleado_habilidad_ibfk_1 FOREIGN KEY (empleado_id) REFERENCES empleado (id),
  CONSTRAINT empleado_habilidad_ibfk_2 FOREIGN KEY (habilidad_id) REFERENCES habilidadesemp (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


