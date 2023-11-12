from datetime import datetime
import json
from unittest import TestCase
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from app import VistaEvaluarCandidato, db, app
from modelos.modelos import Empleado, Empleado_evaluacion

class TestVistaEvaluarCandidato(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_BINDS'] = {
            "empleados": 'sqlite:///:memory:'
        }
        app.config['JWT_SECRET_KEY'] = 'secret'
        self.app = app.test_client()
        self.jwt = JWTManager(app)

        db.session.remove()
        db.drop_all()
        db.create_all()

        self.empleado = Empleado(id=1, nombre='Test Employee')
        db.session.add(self.empleado)
        db.session.commit()

        self.token_de_acceso = create_access_token(identity=123)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + str(self.token_de_acceso)}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_evaluar_candidato_success(self):
        data = {
            "evaluacion": "Good",
            "puntaje": 90
        }
        response = self.app.post('/proyectos/evaluacion/1', data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['candidatos'], 1)

    def test_post_evaluar_candidato_candidato_not_found(self):
        data = {
            "evaluacion": "Good",
            "puntaje": 90
        }
        response = self.app.post('/proyectos/evaluacion/2', data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró el candidato')


