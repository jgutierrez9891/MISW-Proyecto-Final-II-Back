from datetime import datetime
import json
from unittest import TestCase
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test
import mysql.connector

class TestVistaEvaluarCandidato(TestCase):

    def setUp(self):
        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='candidatos',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empleados',
            user='root',
            password='root')

        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='candidatos',
            user='root',
            password=sqlpass)
    
        self.client = app.test_client()
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}

        sql_crear = "INSERT INTO empleados.empleado (id, nombre, num_doc) VALUES (%s, %s, %s)"
        val = (301, "test name","prueba_doc")
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        cursor.close()

    def tearDown(self):
        sql_parent = "DELETE FROM empleados.empleado_evaluacion WHERE empleado_id = 301"
        cursor_parent = self.connection.cursor()
        cursor_parent.execute(sql_parent)
        self.connection.commit()
        cursor_parent.close()
        sql_parent = "DELETE FROM empleados.empleado_habilidad WHERE empleado_id = 301"
        cursor_parent = self.connection.cursor()
        cursor_parent.execute(sql_parent)
        self.connection.commit()
        cursor_parent.close()
        sql_parent = "DELETE FROM empleados.empleado WHERE id = 301"
        cursor_parent = self.connection.cursor()
        cursor_parent.execute(sql_parent)
        self.connection.commit()
        cursor_parent.close()
        super().tearDown()


    def test_1_post_evaluar_candidato_success(self):
        data = {
            "evaluacion": "Good",
            "puntaje": 90
        }
        response = self.client.post('/proyectos/evaluacion/301', data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 201)
        self.assertEqual(data['candidatos'], 301)

    def test_2_post_evaluar_candidato_candidato_not_found(self):
        data = {
            "evaluacion": "Good",
            "puntaje": 90
        }
        response = self.client.post('/proyectos/evaluacion/200004', data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró el candidato')
        
        
    def test_3_consultar_pruebas_candidato_existente(self):
        response = self.client.get("/empleados/prueba_doc", headers={"Authorization": "Bearer " + str(self.token_de_acceso)})
        self.assertEqual(response.status_code, 200)

    def test_4_consultar_pruebas_no_existen_candidato_existente(self):
        response = self.client.get("/empleados/prueba_doc2", headers={"Authorization": "Bearer " + str(self.token_de_acceso)})
        self.assertEqual(response.status_code, 400)



