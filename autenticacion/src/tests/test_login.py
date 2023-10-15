import json
import datetime
from unittest import TestCase
import mysql.connector
from faker import Faker
from faker.generator import random
from app import app, sqlpass


class TestLogin(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()
        
        
        
        connectionCandidatos = mysql.connector.connect(host='34.27.118.190',
        database='candidatos',
        user='root',
        password=sqlpass)
        
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

        cursor = connectionCandidatos.cursor()
        cursor.execute(sql, val)
        connectionCandidatos.commit()
        cursor.close()
        
        
                
        connectionEmpresas = mysql.connector.connect(host='34.27.118.190',
        database='empresas',
        user='root',
        password=sqlpass)
        
        
        #Data Empresa de Prueba
        tipo_docE = 'NIT'
        num_docE = self.data_factory.random_int(min=111111, max=999999)
        nombreE = self.data_factory.first_name()+'-'+self.data_factory.random_int(min=111111, max=999999)
        correoE = self.data_factory.email()
        telefonoE = self.data_factory.phone_number()
        
        sqlInsertEmpresa = "INSERT INTO empresas.empresa (tipo_doc, num_doc, nombre, telefono, email) VALUES (%s, %s, %s, %s, %s)"
        valInsertEmpresa = (tipo_docE, num_docE, nombreE, telefonoE, correoE)
        cursorE = connectionEmpresas.cursor()
        cursorE.execute(sqlInsertEmpresa, valInsertEmpresa)
        connectionEmpresas.commit()
        cursorE.close()
        
        #Data Representante de Prueba
        tipo_docR = 'CC'
        num_docR = self.data_factory.random_int(min=111111, max=999999)
        nombreR = self.data_factory.first_name()+' '+self.data_factory.last_name()
        correoR = self.data_factory.email()
        telefonoR = self.data_factory.phone_number()
        claveR = str(num_doc)
        id_empresaR = 1
        self.userE = correoR
        
        sqlInsertRepresentante = "INSERT INTO empresas.representante (tipo_doc, num_doc, nombre, clave, telefono, email, id_empresa) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valInsertRepresentante = (tipo_docR, num_docR, nombreR, claveR, telefonoR, correoR, ciudad, id_empresaR)
        cursorR = connectionEmpresas.cursor()
        cursorR.execute(sqlInsertRepresentante, valInsertRepresentante)
        connectionEmpresas.commit()
        cursorR.close()
        
        self.datos_loginE = {"usuario": correoR, 
                    "clave": claveR}
         
    #Tests Login Candidatos
    def test_1_login_candidatos_OK(self):
        solicitud_login = self.client.post("/autenticacion/candidatos/login",
                            data=json.dumps(self.datos_login),
                            headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())
        self.assertEqual(solicitud_login.status_code, 200)
        self.assertIsNotNone(respuesta_login["token"])

    def test_2_login_test_1_login_candidatos_OK_ERROR(self):
        datos_login_error = {"usuario": self.usuario, 
                    "clave": "OTRA_CLAVE"}
        solicitud_login = self.client.post("/autenticacion/candidatos/login",
                            data=json.dumps(datos_login_error),
                            headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_login.status_code, 404)
        
        
        
        
    #Tests Login Empresas  
    def test_1_login_candidatos_OK(self):
        solicitud_login = self.client.post("/autenticacion/empresas/login",
                            data=json.dumps(self.datos_loginE),
                            headers={'Content-Type': 'application/json'})
        respuesta_login = json.loads(solicitud_login.get_data())
        self.assertEqual(solicitud_login.status_code, 200)
        self.assertIsNotNone(respuesta_login["token"])

    def test_2_login_test_1_login_candidatos_OK_ERROR(self):
        datos_login_error = {"usuario": self.userE, 
                    "clave": "OTRA_CLAVE"}
        solicitud_login = self.client.post("/autenticacion/candidatos/login",
                            data=json.dumps(datos_login_error),
                            headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_login.status_code, 404)
        
        
        
    def tearDown(self) -> None:
        return super().tearDown()