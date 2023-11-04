import json
from unittest import TestCase
import mysql.connector
from faker import Faker
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test


class TestRol(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='empresas',
            user='root',
            password=sqlpass)
        
        sql = "insert into empresas.representante (tipo_doc, num_doc, nombre, email, telefono, usuario, clave, id_empresa) values ('CC','1023456789','Mauricio Peña', 'mauricio.pena@softwareia.com', '3123456789','maupena', 'miclave123', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (1, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (2, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.proyecto (id, titulo, fecha_inicio, fecha_fin, id_empresa) values (1, '"+self.data_factory.company()+"', '2023-01-01', '2023-01-30', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.proyecto (id, titulo, fecha_inicio, fecha_fin, id_empresa) values (2, '"+self.data_factory.company()+"', '2023-02-01', '2023-03-30', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (1, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (2, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (3, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 2);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) values (4, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 2);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (1, 10);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (1, 20);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (2, 30);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "insert into empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) values (2, 40);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "insert into empresas.rol_ficha_trabajo (id_ficha_trabajo, id_rol) values (1,1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "insert into empresas.rol (id_rol,nombre, descripcion) values (1,'test rol','test desc');"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}
    
    def tearDown(self) -> None:
        sql = "DELETE FROM empresas.ficha_trabajo"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.candidatos_hoja_trabajo"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.hoja_trabajo"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.proyecto"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.rol_ficha_trabajo"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "DELETE FROM empresas.rol"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        return super().tearDown()
    
    def test_6_consultar_rol_equipo(self):
        get_request = self.client.get("/equipos/rol?equipo_id=1",headers=self.headers)
        self.assertEqual(get_request.status_code, 200)

    def test_7_asociar_rol_equipo(self):
        post_request = self.client.post("/equipos/rol/asociar", 
        json={
                "id_rol":1,
                "id_equipo": 1
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 200)

    def test_8_desasociar_rol_equipo(self):
        post_request = self.client.delete("/equipos/rol/asociar", 
        json={
                "id_rol":1,
                "id_equipo": 1
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 200)
        
                
    def tearDown(self) -> None:
        return super().tearDown()