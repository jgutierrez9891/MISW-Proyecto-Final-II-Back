import json
import datetime
from unittest import TestCase
import mysql.connector
from faker import Faker
from faker.generator import random
from app import app, sqlpass


class TestLogin(TestCase):

    def setUp(self):
        connection = mysql.connector.connect(host='34.27.118.190',
        database='candidatos',
        user='root',
        password=sqlpass)

        self.client = app.test_client()
        self.data_factory = Faker()
        tipo_doc = 'CC'
        num_doc = self.data_factory.random_int(min=111111, max=999999)
        nombre = self.data_factory.first_name()+' '+self.data_factory.last_name()
        self.usuario = self.data_factory.first_name()
        clave = self.usuario+str(num_doc)
        telefono = self.data_factory.phone_number()
        correo = self.data_factory.email()
        pais = 'CO'
        ciudad = 'Bogotá'
        aspiracion_salarial = self.data_factory.random_int(min=111111, max=999999)
        fecha_nacimiento = self.data_factory.date_time_between(datetime.datetime.now()+datetime.timedelta(days = (self.data_factory.random_int(min=6570, max=12775))*-1))
        idiomas = 'Español, ingles'

        self.datos_login = {"usuario": self.usuario, 
                    "clave": clave}

        sql = "INSERT INTO candidatos.candidato (tipo_doc, num_doc, nombre, usuario, clave, telefono, email, pais, ciudad, aspiracion_salarial, fecha_nacimiento, idiomas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (tipo_doc, num_doc, nombre, self.usuario, clave, telefono,correo, pais, ciudad, aspiracion_salarial, fecha_nacimiento.strftime("%Y-%m-%d"), idiomas)

        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        
    def tearDown(self) -> None:
        connection = mysql.connector.connect(host='34.27.118.190',
        database='candidatos',
        user='root',
        password=sqlpass)


        sql = "DELETE FROM candidatos.candidato WHERE usuario=%s"
        val = (self.usuario, )

        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()

        return super().tearDown()

    def test_1_login_candidato_OK(self):
        solicitud_login = self.client.post("/autenticacion/candidatos/login",
                            data=json.dumps(self.datos_login),
                            headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())
        self.assertEqual(solicitud_login.status_code, 200)
        self.assertIsNotNone(respuesta_login["token"])

    def test_2_login_candidato_ERROR(self):
        datos_login_error = {"usuario": self.usuario, 
                    "clave": "OTRA_CLAVE"}
        solicitud_login = self.client.post("/autenticacion/candidatos/login",
                            data=json.dumps(datos_login_error),
                            headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_login.status_code, 404)