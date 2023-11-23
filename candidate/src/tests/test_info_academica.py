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
        #Token de autenticación
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}
        self.bad_headers ={'Content-Type': 'application/json'}


    def test_01_success_registrar_InfoAcademica(self):
        json_request = {
            "tipo": "UNIVERSIDAD",
            "valor": "Andes",
            "id_candidato": 1,
            "ano_finalizacion":1987
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 201)
        post_response = json.loads(post_request.get_data())
        self.assertEqual("Informacion registrada exitosamente",post_response.get("message"))
        
    def test_02_fail_campo_no_enviado_InfoAcademica(self):
        json_request = {
            "tipo": "UNIVERSIDAD",
            "valor": "Andes",
            "id_candidato": 1
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        
    def test_03_fail_candidato_no_existe_InfoAcademica(self):
        json_request = {
            "tipo": "UNIVERSIDAD",
            "valor": "Andes",
            "id_candidato": 1000000000000000,
            "ano_finalizacion":1987
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.headers)
        self.assertEqual(post_request.status_code, 409)


    def test_04_fail_no_token_InfoAcademica(self):
        json_request = {
            "tipo": "UNIVERSIDAD",
            "valor": "Andes",
            "id_candidato": 1,
            "ano_finalizacion":1987
        }
        post_request = self.client.post("/candidato/infoAcademica", data=json.dumps(json_request),
                                        headers=self.bad_headers)
        self.assertEqual(post_request.status_code, 401)


    def tearDown(self):
        db.session.close()