from datetime import datetime
import json
from unittest import TestCase
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from app import VistaCandidatosHojas, db, app
from modelos.modelos import Hoja_trabajo, Candidatos_hoja_trabajo, Empleado, Empleado_evaluacion

class TestVistaCandidatosHojas(TestCase):

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

        fecha_inicio = datetime.strptime('2023-01-01', '%Y-%m-%d')
        fecha_fin = datetime.strptime('2023-12-31', '%Y-%m-%d')

        self.hoja = Hoja_trabajo(id=1, nombre_trabajo='Test Job', descripcion_candidato_ideal='Description', id_proyecto=1)
        self.empleado = Empleado(id=1, nombre='Test Employee')
        self.evaluacion = Empleado_evaluacion(id=1, evaluacion='Good', puntaje=90, empleado_id=1)
        self.candidato_hoja = Candidatos_hoja_trabajo(id=1, id_hoja_trabajo=1, id_candidato=1)

        db.session.add(self.hoja)
        db.session.add(self.empleado)
        db.session.add(self.evaluacion)
        db.session.add(self.candidato_hoja)
        db.session.commit()

        self.token_de_acceso = create_access_token(identity=123)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + str(self.token_de_acceso)}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_candidatos_hojas_success(self):
        response = self.app.get('/proyectos/1/hojas-trabajo/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['candidatos']), 1)

    def test_get_candidatos_hojas_hoja_not_found(self):
        response = self.app.get('/proyectos/1/hojas-trabajo/2', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró la hoja de trabajo')

