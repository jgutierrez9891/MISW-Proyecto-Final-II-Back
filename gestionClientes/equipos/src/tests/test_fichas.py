import json
from unittest import TestCase
import mysql.connector
from faker import Faker
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test, rootsqlpass
import random

IP_NO_TEST = "34.27.118.190"
IP_TEST = "0.0.0.0"

class TestFichas(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
        fake = Faker()

        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+rootsqlpass+'@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host=IP_TEST,
            database='empresas',
            user='root',
            password='root')
            self.connection_candidatos = mysql.connector.connect(host=IP_TEST,
            database='candidatos',
            user='root',
            password='root')
        else:
            self.connection = mysql.connector.connect(host=IP_NO_TEST,
            database='empresas',
            user='root',
            password=sqlpass)
            self.connection_candidatos = mysql.connector.connect(host=IP_NO_TEST,
            database='candidatos',
            user='root',
            password=sqlpass)

        #Data para crear candidatos de prueba
        self.tipo_doc_1 = random.choice(["cc","ce","pass"])
        self.tipo_doc_2 = random.choice(["cc","ce","pass"])
        self.num_doc_1 = str(fake.random_number())+str(fake.random_number())
        self.num_doc_2 = str(fake.random_number())+str(fake.random_number())

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
        sql_crear_1 = "INSERT INTO candidatos.candidato (id, tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (100, self.tipo_doc_1, self.num_doc_1, fake.name(), fake.lexify(text = '??????'), fake.lexify(text = '??????'), fake.msisdn(), fake.email(), fake.country(), fake.city(), fake.random_number(), fake.date(), random.choice(['español','inglés','alemán','francés','portuges','italiano']))
        #Crear el candidato en BD
        cursor = self.connection_candidatos.cursor()
        cursor.execute(sql_crear_1, val)
        sql_crear_2 = "INSERT INTO candidatos.candidato (id, tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (200, self.tipo_doc_2, self.num_doc_2, fake.name(), fake.lexify(text = '??????'), fake.lexify(text = '??????'), fake.msisdn(), fake.email(), fake.country(), fake.city(), fake.random_number(), fake.date(), random.choice(['español','inglés','alemán','francés','portuges','italiano']))
        #Crear el candidato en BD
        cursor = self.connection_candidatos.cursor()
        cursor.execute(sql_crear_2, val)
        self.connection_candidatos.commit()
        cursor.close()


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
        sql = "DELETE FROM empresas.candidatos_hoja_trabajo where id_hoja_trabajo in(700,701)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql = "DELETE FROM empresas.candidatos_hoja_trabajo where id_candidato in(100,200)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
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
        sql = "DELETE FROM candidatos.candidato where id in(100,200)"
        cursor = self.connection_candidatos.cursor()
        cursor.execute(sql)
        self.connection_candidatos.commit()
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
    
    def test_8_crear_hoja_trabajo_OK(self):
        datos = {
            "nombre_trabajo": "Test Job 3",
            "descripcion_candidato_ideal": "Description 3",
            "candidatos": [
                {
                    "id": 100
                },
                {
                    "id": 200
                }
            ]
        }
        solicitud_consulta = self.client.post("/proyectos/700/hojas-trabajo",
                                        data=json.dumps(datos),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 201)
    
    def test_8_crear_hoja_trabajo_ERROR_no_existe_candidato(self):
        datos = {
            "nombre_trabajo": "Test Job 3",
            "descripcion_candidato_ideal": "Description 3",
            "candidatos": [
                {
                    "id": 10001
                },
                {
                    "id": 200
                }
            ]
        }
        solicitud_consulta = self.client.post("/proyectos/700/hojas-trabajo",
                                        data=json.dumps(datos),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 404)
        data = json.loads(solicitud_consulta.get_data())
        self.assertEqual(data['message'], 'No se encontró el candidato con id: 10001')
    
    def test_9_crear_hoja_trabajo_ERROR_no_existe_proyecto(self):
        datos = {
            "nombre_trabajo": "Test Job 3",
            "descripcion_candidato_ideal": "Description 3",
            "candidatos": [
                {
                    "id": 10001
                },
                {
                    "id": 200
                }
            ]
        }
        solicitud_consulta = self.client.post("/proyectos/7000/hojas-trabajo",
                                        data=json.dumps(datos),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 404)
        data = json.loads(solicitud_consulta.get_data())
        self.assertEqual(data['message'], 'No se encontró el proyecto')
    
    def test_10_crear_hoja_trabajo_ERROR_datos_incompletos(self):
        datos = {
            "nombre_trabajo": "Test Job 3",
            "candidatos": [
                {
                    "id": 100
                },
                {
                    "id": 200
                }
            ]
        }
        solicitud_consulta = self.client.post("/proyectos/7/hojas-trabajo",
                                        data=json.dumps(datos),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 400)
        data = json.loads(solicitud_consulta.get_data())
        self.assertEqual(data['message'], 'Información incompleta. Asegúrese de enviar los datos esperados')
    
    def test_11_crear_hoja_trabajo_ERROR_datos_vacios(self):
        datos = {
            "nombre_trabajo": "",
            "descripcion_candidato_ideal": "Description 3",
            "candidatos": [
                {
                    "id": 100
                },
                {
                    "id": 200
                }
            ]
        }
        solicitud_consulta = self.client.post("/proyectos/7/hojas-trabajo",
                                        data=json.dumps(datos),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 400)
        data = json.loads(solicitud_consulta.get_data())
        self.assertEqual(data['message'], 'Información incompleta. Asegúrese de enviar los datos esperados')
    
    def test_12_crear_hoja_trabajo_ERROR_candidatos_vacio(self):
        datos = {
            "nombre_trabajo": "Otro trabajo mas",
            "descripcion_candidato_ideal": "Description 3",
            "candidatos": []
        }
        solicitud_consulta = self.client.post("/proyectos/7/hojas-trabajo",
                                        data=json.dumps(datos),
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 400)
        data = json.loads(solicitud_consulta.get_data())
        self.assertEqual(data['message'], 'Información incompleta. Asegúrese de enviar los candidatos')

