import json
from unittest import TestCase
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from app import VistaAsociarEquipoRol, db, app
from modelos.modelos import Candidatos_hoja_trabajo, Ficha_trabajo, Hoja_trabajo, Rol, Rol_ficha_trabajo

class TestVistaAsociarEquipoRol(TestCase):

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
        self.rol1 = Rol(id_rol=1, nombre='Rol1', descripcion='Descripción1')
        self.rol2 = Rol(id_rol=2, nombre='Rol2', descripcion='Descripción1')
        self.equipo1 = Ficha_trabajo(id=1, nombre='Equipo1', descripcion='Descripción1', id_empresa=1, id_proyecto=1)
        self.rol_ficha1 = Rol_ficha_trabajo(id=1, id_ficha_trabajo=1, id_rol=1)

        db.session.add(self.rol1)
        db.session.add(self.rol2)
        db.session.add(self.equipo1)
        db.session.add(self.rol_ficha1)
        db.session.commit()

        hoja_trabajo = Hoja_trabajo(nombre_trabajo='Example', descripcion_candidato_ideal='Description', id_proyecto=1)
        db.session.add(hoja_trabajo)
        db.session.commit()

        candidatos_hoja_trabajo = Candidatos_hoja_trabajo(id_hoja_trabajo=hoja_trabajo.id, id_candidato=1)
        db.session.add(candidatos_hoja_trabajo)
        db.session.commit()       
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                            "Authorization" : "Bearer "+str(self.token_de_acceso)}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_rol_to_equipo_success(self):
        data = {"id_rol": 2, "id_equipo": 1}
        response = self.app.post("/equipos/rol/asociar",headers=self.headers ,data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["Mensaje"], "Rol asociado con Éxito")

    def test_add_rol_to_equipo_duplicate(self):
        data = {"id_rol": 1, "id_equipo": 1}
        response = self.app.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 409)

    def test_add_rol_to_equipo_missing_data(self):
        data = {"id_rol": 1}  # Incomplete data
        response = self.app.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 400)

    def test_add_rol_to_equipo_rol_not_found(self):
        data = {"id_rol": 3, "id_equipo": 1}
        response = self.app.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_add_rol_to_equipo_equipo_not_found(self):
        data = {"id_rol": 1, "id_equipo": 2}
        response = self.app.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_delete_rol_from_equipo_success(self):
        params = {"id_rol": 1, "id_equipo": 1}
        response = self.app.delete("/equipos/rol/asociar", query_string=params,headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["Mensaje"], "Rol desasociado con Éxito")

    def test_delete_rol_from_equipo_not_found(self):
        params = {"id_rol": 3, "id_equipo": 1}
        response = self.app.delete("/equipos/rol/asociar", query_string=params,headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_rol_from_equipo_missing_params(self):
        response = self.app.delete("/equipos/rol/asociar",headers=self.headers)
        self.assertEqual(response.status_code, 400)
