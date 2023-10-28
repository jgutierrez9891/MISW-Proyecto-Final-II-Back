import json
from unittest import TestCase
import mysql.connector
from faker import Faker
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test


class TestFichas(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='empresas',
            user='root',
            password=sqlpass)

        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (1, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "insert into empresas.ficha_trabajo (id, nombre, descripcion, id_empresa) values (2, '"+self.data_factory.company()+"', '"+self.data_factory.company()+"', 1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        self.token_de_acceso = create_access_token(identity=123)

        
    def tearDown(self) -> None:
        sql = "DELETE FROM empresas.ficha_trabajo"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return super().tearDown()
    
    def test_1_obtener_fichas_con_datos_OK(self):
        solicitud_consulta = self.client.get("/equipos/consultar?id_empresa=1",
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        respuesta_consulta = json.loads(solicitud_consulta.get_data())
        self.assertEqual(solicitud_consulta.status_code, 200)
        self.assertIsNotNone(respuesta_consulta["fichas"])
        self.assertEqual(len(respuesta_consulta["fichas"]), 2)
    
    def test_2_obtener_fichas_sin_datosOK(self):
        solicitud_consulta = self.client.get("/equipos/consultar?id_empresa=2",
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 204)
    
    def test_3_obtener_fichas_ERROR_no_idempresa(self):
        solicitud_consulta = self.client.get("/equipos/consultar",
                                        headers={'Content-Type': 'application/json',
                                                 "Authorization" : "Bearer "+str(self.token_de_acceso)})
        self.assertEqual(solicitud_consulta.status_code, 400)

