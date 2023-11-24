from unittest import TestCase
from faker import Faker
from app import app, sqlpass, test
import random
import json
import mysql.connector
from flask_jwt_extended import create_access_token
from modelos import db, candidato, infoLaboral

class TestInfoLaboral(TestCase):
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
        #Token de autenticación
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}
        self.cargo = fake.word()
        self.ano_inicio = fake.random_number()
        self.ano_fin = fake.random_number()
        self.empresa = fake.company()
        self.descripcion = fake.text()

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

    def test_1_success_registrar_InfoLaboral_ConDesc(self):
        json_request = {
            "cargo": self.cargo,
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "descripcion": self.descripcion,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 201)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Informacion registrada exitosamente",post_response.get("message"))
    
    def test_2_success_registrar_InfoLaboral_SinDesc(self):
        json_request = {
            "cargo": self.cargo,
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 201)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Informacion registrada exitosamente",post_response.get("message"))

    def test_3_error_campo_no_enviado(self):
        json_request = {
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Ingrese todos los campos requeridos",post_response.get("message"))
    
    def test_4_error_campo_vacio(self):
        json_request = {
            "cargo": "",
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Campo requerido se encuentra vacío",post_response.get("message"))

    def test_5_error_candidato_no_existe(self):
        json_request = {
            "cargo": self.cargo,
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "id_candidato": str(self.id_candidato)+str(self.id_candidato)
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 409)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("El id_candidato ingresado no existe",post_response.get("message"))
    
    def test_6_error_sin_autenticacion(self):
        json_request = {
            "cargo": self.cargo,
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers={'Content-Type': 'application/json',})
        self.assertEqual(post_request.status_code, 401)
    
    def test_7_consultar_info_laboral_OK(self):

        json_request = {
            "cargo": self.cargo,
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "descripcion": self.descripcion,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 201)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Informacion registrada exitosamente",post_response.get("message"))

        solicitud_consulta = self.client.get("/candidato/infoLaboral?id_candidato="+str(self.id_candidato)+"",
                                             headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 200)
    
    def test_8_consultar_info_laboral_no_existente(self):

        json_request = {
            "cargo": self.cargo,
            "ano_inicio": self.ano_inicio,
            "ano_fin": self.ano_fin,
            "empresa": self.empresa,
            "descripcion": self.descripcion,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoLaboral", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 201)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Informacion registrada exitosamente",post_response.get("message"))

        solicitud_consulta = self.client.get("/candidato/infoLaboral?id_candidato="+str(self.id_candidato)+str(self.id_candidato)+"",
                                             headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_consulta = json.loads(solicitud_consulta.get_data())
        self.assertEqual(solicitud_consulta.status_code, 404)
        self.assertEqual("No se encontró información laboral para el candidato",respuesta_consulta.get("message"))


    def tearDown(self):

        return super().tearDown()