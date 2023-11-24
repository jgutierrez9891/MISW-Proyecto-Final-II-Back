from unittest import TestCase
from faker import Faker
from app import app, sqlpass, test
from modelos import db, candidato, infoAcademica
import random
import json
import mysql.connector
from flask_jwt_extended import create_access_token

class TestInfoAcademica(TestCase):
    def setUp(self):
        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/candidatos'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='candidatos',
            user='root',
            password='root')

        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='candidatos',
            user='root',
            password=sqlpass)

        self.client = app.test_client()
        
        
        fake = Faker()
        #Data para crear usuario de prueba
        self.tipo_doc = random.choice(["cc","ce","pass"])
        self.num_doc = str(fake.random_number())+str(fake.random_number())
        self.nombre = fake.name()
        self.usuario = fake.lexify(text = '??????')
        self.clave = fake.lexify(text = '??????')
        self.telefono = fake.msisdn()
        self.email = fake.email()
        self.pais = fake.country()
        self.city = fake.city()
        self.aspiracion_salarial = fake.random_number()
        self.fecha_nacimiento = fake.date()
        self.idiomas = random.choice(['español','inglés','alemán','francés','portuges','italiano'])

        sql_crear = "INSERT INTO candidatos.candidato (tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.tipo_doc, self.num_doc, self.nombre, self.usuario, self.clave, self.telefono, self.email, self.pais, self.city, self.aspiracion_salarial, self.fecha_nacimiento, self.idiomas)
        #Crear el candidato en BD
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        cursor.close()

        #Consultar el id del candidato
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM candidatos.candidato WHERE num_doc = {self.num_doc}")
        candidatoCreado = cursor.fetchall()
        self.id_candidato = candidatoCreado[0][0]
        self.connection.commit()
        cursor.close()
        #Token de autenticación
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}
        self.bad_headers ={'Content-Type': 'application/json'}


    def test_01_success_registrar_InfoAcademica(self):
        json_request = {
            "institucion":"ANDES",
            "titulo":"UNVIERSITARIO",
            "fecha_inicio":"2017-05-05",
            "fecha_fin":"2023-05-05",
            "id_candidato":self.id_candidato
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 201)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Informacion registrada exitosamente",post_response.get("message"))
        
    def test_02_fail_campo_no_enviado_InfoAcademica(self):
        json_request = json_request = {
            "institucion":"ANDES",
            "titulo":"UNVIERSITARIO",
            "id_candidato":self.id_candidato
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        
    def test_03_fail_candidato_no_existe_InfoAcademica(self):
        json_request = json_request = {
            "institucion":"ANDES",
            "titulo":"UNVIERSITARIO",
            "fecha_inicio":"2017-05-05",
            "fecha_fin":"2023-05-05",
            "id_candidato":10000000000000000
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 409)


    def test_04_fail_no_token_InfoAcademica(self):
        json_request = json_request = {
            "institucion":"ANDES",
            "titulo":"UNVIERSITARIO",
            "fecha_inicio":"2017-05-05",
            "fecha_fin":"2023-05-05",
            "id_candidato":self.id_candidato
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.bad_headers)
        self.assertEqual(post_request.status_code, 401)
        
        
    def test_05_success_consultar_InfoAcademica(self):
        json_request_get = {
            "id_candidato":self.id_candidato
        }
        get_request = self.client.get("/candidato/infoAcademica", data=json.dumps(json_request_get),
                                        headers=self.headers)
        self.assertEqual(get_request.status_code, 200)
        
    def test_06_fail_campo_no_enviado_consultar_InfoAcademica(self):
        json_request_get = {
            "test":self.id_candidato
        }
        post_request = self.client.get("/candidato/infoAcademica", data=json.dumps(json_request_get),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        
    def test_07_fail_candidato_no_existe_consultar_InfoAcademica(self):
        json_request_get = {
            "id_candidato":10000000
        }
        post_request = self.client.get("/candidato/infoAcademica", data=json.dumps(json_request_get),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 409)


    def test_08_fail_no_token_consultar_InfoAcademica(self):
        json_request_get = {
            "id_candidato":10000000
        }
        post_request = self.client.get("/candidato/infoAcademica", data=json.dumps(json_request_get),
                                        headers=self.bad_headers)
        self.assertEqual(post_request.status_code, 401)


    def tearDown(self):
        db.session.close()