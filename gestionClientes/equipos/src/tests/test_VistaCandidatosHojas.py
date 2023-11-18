from datetime import datetime
import json
from unittest import TestCase
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test
import mysql.connector

class TestVistaCandidatosHojas(TestCase):

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
        
        # sql_crear = "REPLACE INTO empresas.proyecto ( id, titulo, id_empresa) VALUES (%s, %s, %s)"
        # val = (770, 'Test', 100)
        # cursor = self.connection.cursor()
        # cursor.execute(sql_crear, val)
        # self.connection.commit()

        sql_child = "DELETE FROM empresas.candidatos_hoja_trabajo WHERE id_hoja_trabajo = 701"
        cursor_child = self.connection.cursor()
        cursor_child.execute(sql_child)
        self.connection.commit()
        cursor_child.close()

        sql_parent = "DELETE FROM empresas.hoja_trabajo WHERE id = 701"
        cursor_parent = self.connection.cursor()
        cursor_parent.execute(sql_parent)
        self.connection.commit()
        cursor_parent.close()

        sql_crear = "INSERT INTO empresas.hoja_trabajo (id, nombre_trabajo, descripcion_candidato_ideal, id_proyecto) VALUES (%s, %s, %s,%s)"
        val = (701,'Test Job 1', 'Description 1', 770)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql_crear = "INSERT INTO empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) VALUES (%s, %s)"
        val = (701, 10)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "REPLACE INTO empresas.candidatos_hoja_trabajo (id_hoja_trabajo, id_candidato) VALUES (%s, %s)"
        val = (701, 20)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql = "DELETE FROM empleados.empleado where id in(10,20)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql_crear = "INSERT INTO empleados.empleado (id, nombre ) VALUES (%s, %s)"
        val = (10, "Nombre1" )
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empleados.empleado (id, nombre ) VALUES (%s, %s)"
        val = (20, "Nombre2" )
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

    def tearDown(self):
        sql = "DELETE FROM empleados.empleado where id in(10,20)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.candidatos_hoja_trabajo where id_hoja_trabajo =701"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.hoja_trabajo WHERE id_proyecto=770"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        # sql = "DELETE FROM empresas.proyecto WHERE id=770"
        # cursor = self.connection.cursor()
        # cursor.execute(sql)
        # self.connection.commit()
        # cursor.close()


    def test_get_candidatos_hojas_success(self):
        response = self.client.get('/proyectos/700/hojas-trabajo/701', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(len(data['candidatos']), 2)

    def test_get_candidatos_hojas_hoja_not_found(self):
        response = self.client.get('/proyectos/1/hojas-trabajo/200', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'No se encontró la hoja de trabajo')

