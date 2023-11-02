from unittest import TestCase
from faker import Faker
from app import app, sqlpass, test
from modelos import db, candidato, infoTecnica
import random
import json
import mysql.connector
from flask_jwt_extended import create_access_token

class TestInfoTecnica(TestCase):
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
        #self.tipo = random.choice(["TECNOLOGIA","LENGUAJE","ROL"])
        self.valor = fake.word()

        #Data para crear usuario de prueba
        self.tipo_doc = random.choice(["cc","ce","pass"])
        self.num_doc = fake.random_number()
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
        
        #Consultar el id del candidato
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM candidatos.candidato WHERE num_doc = {self.num_doc}")
        candidatoCreado = cursor.fetchall()
        self.id_candidato = candidatoCreado[0][0]
        print("el id del candidato es: " + str(candidatoCreado[0][0]))
        cursor.close()

    def test_success_registrar_InfoTecnica(self):
        json_request = {
            "tipo": "TECNOLOGIA",
            "valor": self.valor,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoTecnica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 201)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Informacion registrada exitosamente",post_response.get("message"))

    def test_error_campo_no_enviado(self):
        json_request = {
            "tipo": "LENGUAJE",
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoTecnica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Ingrese todos los campos requeridos",post_response.get("message"))

    def test_error_campo_vacio(self):
        json_request = {
            "tipo": "",
            "valor": self.valor,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoTecnica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Campo requerido se encuentra vacío",post_response.get("message"))

    def test_error_sin_autenticacion(self):
        json_request = {
            "tipo": "ROL",
            "valor": self.valor,
            "id_candidato": self.id_candidato
        }
        post_request = self.client.post("/candidato/infoTecnica", data=json.dumps(json_request),
                                        headers={'Content-Type': 'application/json',})
        self.assertEqual(post_request.status_code, 401)


    def test_error_id_candidato_invalido(self):
        json_request = {
            "tipo": "TECNOLOGIA",
            "valor": self.valor,
            "id_candidato": 0
        }
        post_request = self.client.post("/candidato/infoTecnica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 409)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("El id_candidato ingresado no existe",post_response.get("message"))    




    def tearDown(self):

        """ infosTecnicas = db.session.query(infoTecnica).all()
        for lista in infosTecnicas:
            db.session.delete(lista)
        
        candidatos = db.session.query(candidato).all()
        for lista in candidatos:
            db.session.delete(lista)

        db.session.commit() """
        db.session.close()