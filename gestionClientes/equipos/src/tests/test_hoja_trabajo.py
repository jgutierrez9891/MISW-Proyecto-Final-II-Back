from datetime import datetime
import json
from unittest import TestCase
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from app import VistaHojasTrabajo, db, app
from modelos.modelos import Proyecto, Hoja_trabajo

class TestVistaHojasTrabajo(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['JWT_SECRET_KEY'] = 'secret'
        self.app = app.test_client()
        self.jwt = JWTManager(app)

        db.session.remove()
        db.drop_all()
        db.create_all()

        # Create test data
        fecha_inicio = datetime.strptime('2023-01-01', '%Y-%m-%d')
        fecha_fin = datetime.strptime('2023-12-31', '%Y-%m-%d')

        self.proyecto = Proyecto(id=1100, titulo='Test Project', fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, id_empresa=1)
        self.hoja1 = Hoja_trabajo(id=1, nombre_trabajo='Test Job 1', descripcion_candidato_ideal='Description 1', id_proyecto=1100)
        self.hoja2 = Hoja_trabajo(id=2, nombre_trabajo='Test Job 2', descripcion_candidato_ideal='Description 2', id_proyecto=1100)

        db.session.add(self.proyecto)
        db.session.add(self.hoja1)
        db.session.add(self.hoja2)
        db.session.commit()

        self.token_de_acceso = create_access_token(identity=123)
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + str(self.token_de_acceso)}

    

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_hojas_trabajo_success(self):
        response = self.app.get('/proyectos/1100/hojas-trabajo', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['hojasDetrabajo']), 2)

    def test_get_hojas_trabajo_proyecto_not_found(self):
        response = self.app.get('/proyectos/2/hojas-trabajo', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró el proyecto')

    # Add more test cases as needed
