import json
import random
from unittest import TestCase
from faker import Faker
from app import app, sqlpass, test
from modelos import db, candidato, entrevista
import mysql.connector
from flask_jwt_extended import create_access_token

class TestCandidate(TestCase):
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
        self.valor = fake.word()
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}

        #Data para las pruebas
        self.tipo_doc = random.choice(["cc","ce","pass"])
        self.num_doc = fake.random_int(1023884000,1023885000)
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
        self.resultado = fake.random_int(1,100)
        self.id_empresa = fake.random_int(2000,3000)

        #Crear el candidato en BD
        sql_crear = "INSERT INTO candidatos.candidato (tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.tipo_doc, self.num_doc, self.nombre, self.usuario, self.clave, self.telefono, self.email, self.pais, self.city, self.aspiracion_salarial, self.fecha_nacimiento, self.idiomas)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        #Consultar el id del candidato
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM candidatos.candidato WHERE num_doc = {self.num_doc}")
        candidatoCreado = cursor.fetchall()
        self.id_candidato = candidatoCreado[0][0]
        cursor.close()

        #Crear entrevista en BD
        sql_crear = "INSERT INTO candidatos.entrevista (id_candidato, fecha, estado, nombre_entrevista, resultado, id_empresa) values (%s, %s, %s, %s, %s, %s)"
        val = (self.id_candidato, fake.date(), "finalizada", self.idiomas, self.resultado, self.id_empresa)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

    def test_success_consultar_entrevista(self):

        get_request = self.client.get("/candidato/resultadosEntrevistas", query_string = {"tipo_doc":self.tipo_doc,"num_doc":self.num_doc,"id_empresa":self.id_empresa},
                                             headers=self.headers)
        self.assertEqual(get_request.status_code, 200)
        get_response = json.loads(get_request.get_data())
        self.assertIsNotNone(get_response.get("message"))

    def test_error_tipodoc_no_enviado(self):

        get_request = self.client.get("/candidato/resultadosEntrevistas", query_string = {"num_doc":self.num_doc,"id_empresa":self.id_empresa},
                                             headers=self.headers)
        self.assertEqual(get_request.status_code, 400)
        get_response = json.loads(get_request.get_data())
        self.assertEqual("Debe ingresar el tipo de doc del candidato",get_response.get("message"))

    def test_error_numdoc_no_enviado(self):

        get_request = self.client.get("/candidato/resultadosEntrevistas", query_string = {"tipo_doc":self.tipo_doc,"id_empresa":self.id_empresa},
                                             headers=self.headers)
        self.assertEqual(get_request.status_code, 400)
        get_response = json.loads(get_request.get_data())
        self.assertEqual("Debe ingresar el doc del candidato",get_response.get("message"))

    def test_error_idempresa_no_enviado(self):

        get_request = self.client.get("/candidato/resultadosEntrevistas", query_string = {"tipo_doc":self.tipo_doc,"num_doc":self.num_doc},
                                             headers=self.headers)
        self.assertEqual(get_request.status_code, 400)
        get_response = json.loads(get_request.get_data())
        self.assertEqual("Debe ingresar el id de la empresa",get_response.get("message"))

    def test_error_no_existen_entrevistas(self):

        get_request = self.client.get("/candidato/resultadosEntrevistas", query_string = {"tipo_doc":self.tipo_doc,"num_doc":10547834934,"id_empresa":self.id_empresa},
                                             headers=self.headers)
        self.assertEqual(get_request.status_code, 409)
        get_response = json.loads(get_request.get_data())
        self.assertEqual("No existen datos para el documento ingresado",get_response.get("message"))

    def test_error_candidato_no_tiene_entrevistas(self):

        get_request = self.client.get("/candidato/resultadosEntrevistas", query_string = {"tipo_doc":self.tipo_doc,"num_doc":self.num_doc,"id_empresa":1990},
                                             headers=self.headers)
        self.assertEqual(get_request.status_code, 200)
        get_response = json.loads(get_request.get_data())
        self.assertEqual("El candidato seleccionado no tiene entrevistas finalizadas",get_response.get("message"))  


    def tearDown(self):

        entrevistas = db.session.query(entrevista).all()
        for lista in entrevistas:
            if lista.id_empresa == self.id_empresa:
                db.session.delete(lista)

        candidatos = db.session.query(candidato).all()
        for lista in candidatos:
            if lista.id == self.id_candidato:
                db.session.delete(lista)

        db.session.commit()
        db.session.close()
