import json
import datetime
from unittest import TestCase
import mysql.connector
from faker import Faker
from modelos.modelos import db, Representante, Empresa
from app import app, sqlpass, test


class TestLogin(TestCase):

    def setUp(self):
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

        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()
        
        
    #PRUEBAS AUTENTIACION COMO EMPRESA
    def test_1_login_empresa_OK(self):
        post_request = self.client.post("/autenticacion/empresas/login", json={"usuario":"maupena","clave":"miclave123"})
        self.assertEqual(post_request.status_code, 200)

    def test_2_login_empresa_404(self):
        post_request = self.client.post("/autenticacion/empresas/login", json={"usuario" : "mauspena", "clave" : "miclave123s"})
        self.assertEqual(post_request.status_code, 404)
        
    def test_3_login_empresa_400(self):
        post_request = self.client.post("/autenticacion/empresas/login", json={"usuarios" : "maupena", "clave" : "miclave123"})
        self.assertEqual(post_request.status_code, 400)


    #PRUEBAS AUTENTIACION COMO CANDIDATO
    def test_4_login_candidato_OK(self):
        solicitud_login = self.client.post("/autenticacion/candidatos/login",
                            data=json.dumps(self.datos_login),
                            headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())
        self.assertEqual(solicitud_login.status_code, 200)
        self.assertIsNotNone(respuesta_login["token"])

    def test_5_login_candidato_ERROR(self):
        datos_login_error = {"usuario": self.usuario, 
                    "clave": "OTRA_CLAVE"}
        solicitud_login = self.client.post("/autenticacion/candidatos/login",
                            data=json.dumps(datos_login_error),
                            headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_login.status_code, 404)       
        
    #TEARDOWN
    def tearDown(self) -> None:
        representantes = db.session.query(Representante).all()
        for item in representantes:
            db.session.delete(item)
            
        empresas = db.session.query(Empresa).all()
        for item in empresas:
            db.session.delete(item)
            
        sql = "DELETE FROM candidatos.candidato WHERE usuario=%s"
        val = (self.usuario, )

        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()
        
        return super().tearDown()