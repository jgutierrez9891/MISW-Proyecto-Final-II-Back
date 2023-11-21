import json
from unittest import TestCase
import mysql.connector
from faker import Faker
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test, rootsqlpass


class TestFichas(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+rootsqlpass+'@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='empresas',
            user='root',
            password=sqlpass)

        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (1, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()        
        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (2, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "insert into empresas.empleado_ficha_trabajo (id_ficha_trabajo, id_empleado) values (1, 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "insert into empresas.empleado_ficha_trabajo (id_ficha_trabajo, id_empleado) values (2, 2);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql_crear = "INSERT INTO empresas.empresa (id, tipo_doc, num_doc, nombre, email, telefono) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (100, "Test", "Test", "Test", "Test", "Test")
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        cursor.close()
        sql_crear = "INSERT INTO empresas.proyecto ( id, titulo, id_empresa) VALUES (%s, %s, %s)"
        val = (700, 'Test', 100)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        cursor.close()
        sql_crear = "INSERT INTO empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) VALUES (%s, %s, %s,%s)"
        val = (7010,'Test Job 1', 'Description 1', 700)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        cursor.close()
        sql_crear = "INSERT INTO empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) VALUES (%s, %s, %s,%s)"
        val = (7011,'Test Job 2', 'Description 2', 700)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        cursor.close()
        sql_crear = "INSERT INTO empresas.proyecto ( id, titulo, id_empresa) VALUES (%s, %s, %s)"
        val = (770, 'Test', 100)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) VALUES (%s, %s, %s,%s)"
        val = (701,'Test Job 1', 'Description 1', 770)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) VALUES (%s, %s)"
        val = (701, 10)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) VALUES (%s, %s)"
        val = (701, 20)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empleados.empleado (id, nombre ) VALUES (%s, %s)"
        val = (10, "Nombre1" )
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empleados.empleado (id, nombre ) VALUES (%s, %s)"
        val = (20, "Nombre2" )
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}

        
    def tearDown(self) -> None:
        sql = "DELETE FROM empresas.empleado_ficha_trabajo where id_ficha_trabajo in(1,2)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.rol_ficha_trabajo WHERE id_ficha_trabajo in(1,2)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.candidatos_hoja_trabajo where id_hoja_trabajo =701"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        cursor.close()
        sql_parent = "DELETE FROM empresas.hoja_trabajo WHERE id = 701"
        cursor_parent = self.connection.cursor()
        cursor_parent.execute(sql_parent)
        self.connection.commit()
        cursor_parent.close()
        sql = "DELETE FROM empresas.ficha_trabajo WHERE id in (1,2)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.ficha_trabajo WHERE id_empresa=101"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.hoja_trabajo WHERE id_proyecto in(700,770)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.proyecto WHERE id in(700,770)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empleados.empleado where id in(10,20)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.empresa WHERE id in(100,101)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        
        return super().tearDown()    

    
    def test_1_obtener_fichas_sin_datosOK(self):
        solicitud_consulta = self.client.get("/equipos/consultar?id_empresa=2",
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 204)
    
    def test_2_obtener_fichas_con_datos_OK(self):
        solicitud_consulta = self.client.get("/equipos/consultar?id_empresa=1",
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_consulta = json.loads(solicitud_consulta.get_data())
        self.assertEqual(solicitud_consulta.status_code, 200)
        self.assertIsNotNone(respuesta_consulta["fichas"])
        self.assertEqual(len(respuesta_consulta["fichas"]), 2)
    
    def test_3_obtener_fichas_ERROR_no_idempresa(self):
        solicitud_consulta = self.client.get("/equipos/consultar",
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 400)
    
    def test_4_get_hojas_trabajo_success(self):
        response = self.client.get('/proyectos/700/hojas-trabajo', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['hojasDetrabajo']), 2)

    def test_5_get_hojas_trabajo_proyecto_not_found(self):
        response = self.client.get('/proyectos/1102/hojas-trabajo', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró el proyecto')

    def test_6_get_candidatos_hojas_success(self):
        response = self.client.get('/proyectos/770/hojas-trabajo/701', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['candidatos']), 2)

    def test_7_get_candidatos_hojas_hoja_not_found(self):
        response = self.client.get('/proyectos/1/hojas-trabajo/200', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró la hoja de trabajo')

