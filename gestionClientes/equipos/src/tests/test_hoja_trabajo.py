import json
from unittest import TestCase
from flask_jwt_extended import  create_access_token
from app import app, sqlpass, test
import mysql.connector

class TestVistaHojasTrabajo(TestCase):

    def setUp(self):
        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/candidatos'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='candidatos',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empleados',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
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

        sql_crear = "INSERT INTO empresas.hoja_trabajo ( nombre_trabajo, descripcion_candidato_ideal, id_proyecto) VALUES (%s, %s, %s)"
        val = ('Test Job 1', 'Description 1', 7)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

    

    def tearDown(self):
        sql = "DELETE FROM empresas.hoja_trabajo WHERE id_proyecto=7"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def test_get_hojas_trabajo_success(self):
        response = self.client.get('/proyectos/7/hojas-trabajo', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['hojasDetrabajo']), 1)

    def test_get_hojas_trabajo_proyecto_not_found(self):
        response = self.client.get('/proyectos/1102/hojas-trabajo', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró el proyecto')

