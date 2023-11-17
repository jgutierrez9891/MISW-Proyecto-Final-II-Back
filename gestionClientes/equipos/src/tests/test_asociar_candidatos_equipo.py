import json
from unittest import TestCase
from flask_jwt_extended import create_access_token
import mysql.connector
from app import app, test, sqlpass
import random
import json
from faker import Faker

IP_NO_TEST = "34.27.118.190"
IP_TEST = "0.0.0.0"

class TestAsociarCandidatosAEquipo(TestCase):    

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
        fake = Faker()

        self.token_de_acceso = create_access_token(identity=123)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + str(self.token_de_acceso)}
        
        if test:
            self.connection_empresas = mysql.connector.connect(host=IP_TEST,
            database='empresas',
            user='root',
            password='root')
            self.connection_candidatos = mysql.connector.connect(host=IP_TEST,
            database='candidatos',
            user='root',
            password='root')
            self.connection_empleados = mysql.connector.connect(host=IP_TEST,
            database='empleados',
            user='root',
            password='root')
        else:
            self.connection_empresas = mysql.connector.connect(host=IP_NO_TEST,
            database='empresas',
            user='root',
            password=sqlpass)
            self.connection_candidatos = mysql.connector.connect(host=IP_NO_TEST,
            database='candidatos',
            user='root',
            password=sqlpass)
            self.connection_empleados = mysql.connector.connect(host=IP_NO_TEST,
            database='empleados',
            user='root',
            password=sqlpass)
        
        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (100, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection_empresas.cursor()
        cursor.execute(sql)
        self.connection_empresas.commit()

        #Data para crear candidatos de prueba
        self.tipo_doc_1 = random.choice(["cc","ce","pass"])
        self.tipo_doc_2 = random.choice(["cc","ce","pass"])
        self.num_doc_1 = str(fake.random_number())+str(fake.random_number())
        self.num_doc_2 = str(fake.random_number())+str(fake.random_number())

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

    def tearDown(self):
        sql = "DELETE FROM empresas.empleado_ficha_trabajo where id_ficha_trabajo=100"
        cursor = self.connection_empresas.cursor()
        cursor.execute(sql)
        self.connection_empresas.commit()
        cursor.close()
        sql = "DELETE FROM empresas.ficha_trabajo where id=100"
        cursor = self.connection_empresas.cursor()
        cursor.execute(sql)
        self.connection_empresas.commit()
        cursor.close()
        sql = "DELETE FROM candidatos.candidato where id in(100,200)"
        cursor = self.connection_candidatos.cursor()
        cursor.execute(sql)
        self.connection_candidatos.commit()
        cursor.close()
        sql = "DELETE FROM empleados.empleado"
        cursor = self.connection_empleados.cursor()
        cursor.execute(sql)
        self.connection_empleados.commit()
        cursor.close()
        return super().tearDown()

    def test_1_asociar_un_candidato_ok(self):
        lista_candidatos = {
            "candidatos": [
                {
                    "id_candidato": "100"
                }
            ]
        }
        solicitud_asociacion = self.client.post('/equipos/100/candidatos', data=json.dumps(lista_candidatos),
                                 headers=self.headers)
        respuesta_asociacion = json.loads(solicitud_asociacion.get_data())
        self.assertEqual(solicitud_asociacion.status_code, 200)
        self.assertEqual(respuesta_asociacion["message"], "Candidatos asociados con éxito")

    def test_2_asociar_dos_candidato_ok(self):
        lista_candidatos = {
            "candidatos": [
                {
                    "id_candidato": "100"
                },
                {
                    "id_candidato": "200" 
                }
            ]
        }
        solicitud_asociacion = self.client.post('/equipos/100/candidatos', data=json.dumps(lista_candidatos),
                                 headers=self.headers)
        respuesta_asociacion = json.loads(solicitud_asociacion.get_data())
        self.assertEqual(solicitud_asociacion.status_code, 200)
        self.assertEqual(respuesta_asociacion["message"], "Candidatos asociados con éxito")

    def test_3_asociar_candidatos_ERROR_no_existe_equipo(self):
        lista_candidatos = {
            "candidatos": [
                {
                    "id_candidato": "100"
                },
                {
                    "id_candidato": "200" 
                }
            ]
        }
        solicitud_asociacion = self.client.post('/equipos/200/candidatos', data=json.dumps(lista_candidatos),
                                headers=self.headers)
        respuesta_asociacion = json.loads(solicitud_asociacion.get_data())
        self.assertEqual(solicitud_asociacion.status_code, 404)
        self.assertEqual(respuesta_asociacion["message"], "No se encontró el equipo")
    
    def test_4_asociar_candidato_ERROR_no_info_candidatos(self):
        lista_candidatos = {
        }
        solicitud_asociacion = self.client.post('/equipos/100/candidatos', data=json.dumps(lista_candidatos),
                                 headers=self.headers)
        respuesta_asociacion = json.loads(solicitud_asociacion.get_data())
        self.assertEqual(solicitud_asociacion.status_code, 400)
        self.assertEqual(respuesta_asociacion["message"], "Información incompleta. Asegúrese de enviar los datos esperados")

    def test_5_asociar_candidato_ERROR_no_info_candidatos2(self):
        lista_candidatos = {
            "candidatos": []
        }
        solicitud_asociacion = self.client.post('/equipos/100/candidatos', data=json.dumps(lista_candidatos),
                                 headers=self.headers)
        respuesta_asociacion = json.loads(solicitud_asociacion.get_data())
        self.assertEqual(solicitud_asociacion.status_code, 400)
        self.assertEqual(respuesta_asociacion["message"], "Información incompleta. Asegúrese de enviar los datos esperados")
    
    def test_6_asociar_candidato_ERROR_candidato_no_existe(self):
        lista_candidatos = {
            "candidatos": [
                {
                    "id_candidato": "1001"
                },
                {
                    "id_candidato": "200" 
                }
            ]
        }
        solicitud_asociacion = self.client.post('/equipos/100/candidatos', data=json.dumps(lista_candidatos),
                                 headers=self.headers)
        self.assertEqual(solicitud_asociacion.status_code, 404)
