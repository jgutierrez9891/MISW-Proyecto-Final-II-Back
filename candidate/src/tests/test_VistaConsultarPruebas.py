from unittest import TestCase
from flask_jwt_extended import create_access_token
from modelos import db
from app import app, sqlpass, test
import mysql.connector

class TestVistaConsultarPruebas(TestCase):

    def setUp(self):
        # Set up the Flask app for testing
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
        cursor = self.connection.cursor()
        
        sql_delete_resultado = "DELETE FROM candidatos.resultado_prueba_tecnica WHERE candidato_id in (1001,1002)"
        cursor.execute(sql_delete_resultado)
        self.connection.commit()

        sql_delete_candidato = "DELETE FROM candidatos.candidato WHERE id in (1001,1002)"
        cursor.execute(sql_delete_candidato)
        self.connection.commit()

        sql_crear_candidato = """
            INSERT INTO candidatos.candidato 
            (id, tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas, estado) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        val_candidato = (1001, "cc", "123456789", "John Doe", "john_doe", "password", "1234567890", "john.doe@example.com", "USA", "New York", 50000, "1990-01-15", "English, Spanish", "DISPONIBLE")

        sql_crear_candidato2 = """
            INSERT INTO candidatos.candidato 
            (id, tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas, estado) 
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        val_candidato2 = (1002, "cc", "abc123456", "Doe manuel", "doe_manuel", "password", "1234567890", "doe.manuel@example.com", "Canada", "Toronto", 50000, "1990-01-15", "English, Spanish", "DISPONIBLE")

        sql_crear_resultado = """
            INSERT INTO candidatos.resultado_prueba_tecnica 
            (id, candidato_id, nombre, fecha_prueba, puntaje) 
            VALUES 
            (%s, %s, %s, %s, %s)
        """

        val_resultado = (1001, 1001, "Prueba A", "2023-01-01", 80)

        cursor.execute(sql_crear_candidato, val_candidato)
        self.connection.commit()

        cursor.execute(sql_crear_candidato2, val_candidato2)
        self.connection.commit()

        cursor.execute(sql_crear_resultado, val_resultado)
        self.connection.commit()

        self.token = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                "Authorization" : "Bearer "+str(self.token)}
        
    # def tearDown(self):
    #     sql = "DELETE FROM candidatos.resultado_prueba_tecnica WHERE candidato_id=100"
    #     cursor = self.connection.cursor()
    #     cursor.execute(sql)
    #     self.connection.commit()
    #     cursor.close()
    #     sql = "DELETE FROM candidatos.info_tecnica WHERE id_candidato=100"
    #     cursor = self.connection.cursor()
    #     cursor.execute(sql)
    #     self.connection.commit()
    #     cursor.close()
    #     sql = "DELETE FROM candidatos.info_academica WHERE id_candidato=100"
    #     cursor = self.connection.cursor()
    #     cursor.execute(sql)
    #     self.connection.commit()
    #     cursor.close()
    #     sql = "DELETE FROM candidatos.info_laboral WHERE id_candidato=100"
    #     cursor = self.connection.cursor()
    #     cursor.execute(sql)
    #     self.connection.commit()
    #     cursor.close()
    #     sql = "DELETE FROM candidatos.candidato WHERE id = 100"
    #     cursor = self.connection.cursor()
    #     cursor.execute(sql)
    #     self.connection.commit()
    #     cursor.close()



    def test_consultar_pruebas_candidato_existente(self):
        response = self.client.get("/candidato/pruebas/123456789", headers={"Authorization": "Bearer " + str(self.token)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["pruebas"]), 1)
        self.assertEqual(response.json["pruebas"][0]["nombre"], "Prueba A")

    def test_consultar_pruebas_no_existen_candidato_existente(self):
        response = self.client.get("/candidato/pruebas/abc123456", headers={"Authorization": "Bearer " + str(self.token)})
        self.assertEqual(response.status_code, 204)

    def test_consultar_pruebas_candidato_no_existente(self):
        response = self.client.get("/candidato/pruebas/987654321", headers={"Authorization": "Bearer " + str(self.token)})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "Candidato no encontrado")
