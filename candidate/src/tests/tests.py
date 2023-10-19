from unittest import TestCase
from faker import Faker
from app import app
from modelos import db, candidato, candidatoSchema
import random
import json
import time

class TestGetPostByID(TestCase):
    def setUp(self):
        self.client = app.test_client()
        fake = Faker()
        self.tipo_doc = random.choice(["cc","ce","pass"])
        self.num_doc = fake.random_number()
        self.nombre = fake.name()
        self.usuario = fake.lexify(text = '??????')
        self.clave = fake.lexify(text = '??????')
        self.telefono = fake.msisdn()
        self.email = fake.email()
        self.email_invalido = random.choice(['pruebagmail.com','prueba@gmailcom','prueba@gmail.','@gmail.com'])
        self.pais = fake.country()
        self.city = fake.city()
        self.aspiracion_salarial = fake.random_number()
        self.fecha_nacimiento = fake.date()
        self.idiomas = random.choice(['español','inglés','alemán','francés','portuges','italiano'])


    def test_ping(self):
        ping_request = self.client.get("/candidato/ping")
        self.assertEqual(ping_request.status_code, 200)

    def test_createCandidate(self):
        json_request = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }
        post_request = self.client.post("/candidato/create", json=json_request)
        self.assertEqual(post_request.status_code, 200)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Candidato creado exitosamente",post_response.get("message"))

    def test_campoRequeridoVacio(self):
        json_request = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc,
            "nombre": "",
            "usuario": self.usuario,
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }
        post_request = self.client.post("/candidato/create", json=json_request)
        self.assertEqual(post_request.status_code, 400)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Debe ingresar todos los campos",post_response.get("message"))

    def test_correoInvalido(self):
        json_request = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email_invalido,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }
        post_request = self.client.post("/candidato/create", json=json_request)
        self.assertEqual(post_request.status_code, 400)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("El formato del correo es inválido",post_response.get("message"))


    def test_numDocExiste(self):
        json_request = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }
        post_request_1 = self.client.post("/candidato/create", json=json_request)
        self.assertEqual(post_request_1.status_code, 200)

        post_request_2 = self.client.post("/candidato/create", json=json_request)

        self.assertEqual(post_request_2.status_code, 409)
        post_response = json.loads(post_request_2.get_data())
        self.assertEqual("El documento ingresado ya existe",post_response.get("message"))

    def test_usuarioExiste(self):
        json_request_user1 = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }
        post_request_1 = self.client.post("/candidato/create", json=json_request_user1)
        self.assertEqual(post_request_1.status_code, 200)

        json_request_user2 = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc + 123,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }

        post_request_2 = self.client.post("/candidato/create", json=json_request_user2)

        self.assertEqual(post_request_2.status_code, 409)
        post_response = json.loads(post_request_2.get_data())
        self.assertEqual("El usuario ingresado ya existe",post_response.get("message"))

    def test_correoExiste(self):
        json_request_user1 = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }
        post_request_1 = self.client.post("/candidato/create", json=json_request_user1)
        self.assertEqual(post_request_1.status_code, 200)

        json_request_user2 = {
            "tipo_doc": self.tipo_doc,
            "num_doc": self.num_doc + 123,
            "nombre": self.nombre,
            "usuario": self.usuario + "ca",
            "clave": self.clave,
            "telefono": self.telefono,
            "email": self.email,
            "pais": self.pais,
            "ciudad": self.city,
            "aspiracion_salarial": self.aspiracion_salarial,
            "fecha_nacimiento": self.fecha_nacimiento,
            "idiomas": self.idiomas
        }

        post_request_2 = self.client.post("/candidato/create", json=json_request_user2)

        self.assertEqual(post_request_2.status_code, 409)
        post_response = json.loads(post_request_2.get_data())
        self.assertEqual("El correo ingresado ya existe",post_response.get("message"))
        
    def test_historial_entrevistas_candidato_NO_existe(self):
        json_request_user1 = {
            "id_candidato":10
        }
        post_request_1 = self.client.get("/candidato/historialEntrevistas", json=json_request_user1)
        self.assertEqual(post_request_1.status_code, 200)
        
    def test_historial_entrevistas_candidato_SI_existe(self):
        json_request_user1 = {
            "id_candidato":1
        }
        post_request_1 = self.client.get("/candidato/historialEntrevistas", json=json_request_user1)
        self.assertEqual(post_request_1.status_code, 200)
        
    def test_historial_entrevistas_bad_request(self):
        json_request_user1 = {
            "a":1
        }
        post_request_1 = self.client.get("/candidato/historialEntrevistas", json=json_request_user1)
        self.assertEqual(post_request_1.status_code, 400)

    def tearDown(self):
       
        candidatos = db.session.query(candidato).all()
        for lista in candidatos:
            db.session.delete(lista)

        db.session.commit()
        db.session.close()